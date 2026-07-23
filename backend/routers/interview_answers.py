from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_candidate_by_token
from services.consent import ConsentRequiredError
from services.interview_answers import (
    notify_interview_finished_background,
    process_answer_background,
    save_answer,
)

router = APIRouter(prefix="/candidates", tags=["interview_answers"])


class AnswerOut(BaseModel):
    answer_id: int
    audio_path: str
    # Round-3 follow-up #22 (2026-07-19): transcript_text removed — transcription now happens in
    # a background task AFTER this response is sent, so it doesn't exist yet at response time.
    # Confirmed no caller reads it from this endpoint's response (CandidateDetailPage.tsx's
    # transcript_text comes from a different endpoint, candidate_detail.py's AnswerDetailOut).


class CandidateQuestionOut(BaseModel):
    id: int
    question_text: str
    order_index: int
    duration_seconds: int

    class Config:
        from_attributes = True


@router.get("/{candidate_id}/questions", response_model=list[CandidateQuestionOut])
def list_candidate_questions(candidate_id: int, token: str, db: Session = Depends(get_db)):
    """Candidate-facing (token-authenticated). Only ever returns approved questions —
    candidates never see drafts. Each question now carries its own HR-set time limit
    (2026-07-19 follow-up, replacing the earlier job-wide-only duration) — the video recorder
    reads duration_seconds off the current question, not a single job-level value."""
    candidate = get_candidate_by_token(token, db)
    if candidate.id != candidate_id:
        raise HTTPException(status_code=401, detail="Token does not match this candidate")

    questions = repo.interview_questions.list(db, job_id=candidate.job_id, status="approved")
    return sorted(questions, key=lambda q: q.order_index)


@router.post("/{candidate_id}/answers", response_model=AnswerOut)
async def submit_interview_answer(
    candidate_id: int,
    background_tasks: BackgroundTasks,
    question_id: int = Form(...),
    session: str = Form(...),
    token: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Candidate-facing (token-authenticated, not HR JWT). Consent-gated: 403 without a
    consent_records row for this candidate.

    Round-3 follow-up #22 (2026-07-19): only saves the video synchronously now — transcription +
    rubric scoring (the slow part, 10-20+ seconds per answer) run afterward as a BackgroundTask,
    so this response returns as soon as the file is on disk. User-reported problem this fixes:
    with all 4 answers now uploaded sequentially at the end of the interview (T17-followup #21),
    the candidate was stuck watching "Mengunggah jawaban N dari 4..." for the FULL synchronous
    pipeline time of every single answer, back to back.

    2026-07-22 (user decision, reversing an earlier attempt at a blocking "please wait" screen):
    the candidate is released the moment their video data is confirmed stored — not once the
    LLM chain (transcription/scoring/summary/upskilling plan) finishes. That pipeline now runs
    fully invisibly in the background; only HR-facing surfaces (Laporan list, report page) gate on
    it actually completing (routers/jobs.py's processing_complete, routers/report.py's
    _require_report_ready)."""
    candidate = get_candidate_by_token(token, db)
    if candidate.id != candidate_id:
        raise HTTPException(status_code=401, detail="Token does not match this candidate")

    audio_bytes = await file.read()

    try:
        answer = save_answer(db, candidate_id, question_id, audio_bytes, session)
    except ConsentRequiredError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    background_tasks.add_task(process_answer_background, answer.id, candidate_id)

    # The "terima kasih sudah wawancara" email fires here — as soon as this was the LAST approved
    # question's video to land on disk — not after the LLM chain finishes. Guarded by
    # interview_finished_notified_at inside the notification function itself, so re-submitting an
    # already-answered question (save_answer's resubmission path) can't send it twice.
    approved_questions = repo.interview_questions.list(db, job_id=candidate.job_id, status="approved")
    all_answers = repo.interview_answers.list(db, candidate_id=candidate_id)
    if approved_questions and len(all_answers) >= len(approved_questions):
        background_tasks.add_task(notify_interview_finished_background, candidate_id)

    return AnswerOut(answer_id=answer.id, audio_path=answer.audio_path)
