from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.interview_questions import generate_one_question

router = APIRouter(prefix="/jobs", tags=["interview_questions"])

# Job-level default duration was removed 2026-07-19 (superseded by per-question durations,
# see QuestionDurationRequest below) — this is the fallback for a brand-new question whose
# duration wasn't explicitly set by the frontend, matching the model column's own default.
_DEFAULT_QUESTION_DURATION_SECONDS = 120


class QuestionOut(BaseModel):
    id: int
    job_id: int
    question_text: str
    order_index: int
    status: str
    duration_seconds: int

    class Config:
        from_attributes = True


class QuestionUpdateItem(BaseModel):
    id: int | None = None  # None = new question to add
    question_text: str
    order_index: int
    # Only meaningful when id is None (a brand-new question) — the frontend's locally-chosen
    # duration for a not-yet-persisted draft. Ignored for existing ids: their real duration_seconds
    # (possibly changed via PATCH .../duration since the last load) is preserved instead, see below.
    duration_seconds: int | None = None


class QuestionsUpdateRequest(BaseModel):
    questions: list[QuestionUpdateItem]


class QuestionDurationRequest(BaseModel):
    duration_seconds: int


class GeneratedQuestionOut(BaseModel):
    question: str


class GenerateQuestionRequest(BaseModel):
    # This slot's own current text, if any — used as the specific topic to build the question
    # around (a real finding: discarding this and generating a generic JD-grounded question
    # instead produced results completely unrelated to what HR had written for that slot). None
    # or blank/whitespace-only means "no hint, generate a plain JD-grounded question."
    hint: str | None = None
    # The question texts HR is keeping (unchecked slots) PLUS every question already generated so
    # far in this same multi-slot request (the frontend accumulates and resends this on each call)
    # — passed as context so the model doesn't generate a question that thematically overlaps.
    existing_questions: list[str] = []


def _get_scoped_job(db: Session, job_id: int, company_id: int):
    job = repo.jobs.get(db, job_id)
    if not job or job.company_id != company_id:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/questions/generate", response_model=GeneratedQuestionOut)
def generate_job_question(
    job_id: int, body: GenerateQuestionRequest, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """Stateless (2026-07-19 follow-up, user-requested): generates ONE question TEXT via Flash and
    returns it WITHOUT writing anything to the database. AI-suggested drafts now live purely in
    frontend state until HR clicks "Setujui & Kunci Pertanyaan" (PUT /questions then POST
    /questions/approve) — matching how manually-typed drafts (via "+ Tambah Pertanyaan") already
    only ever get persisted at that point.

    Generates exactly ONE question per call, not a batch — a single-prompt "generate all N, stay
    distinct" attempt was tried first but the user found the real-world results still
    inconsistent/mixed/unrelated. The frontend now calls this endpoint once per requested question,
    IN ORDER, accumulating results into body.existing_questions on each subsequent call (so
    distinctness is enforced by construction) — deliberately client-driven rather than looped
    server-side so the UI can show live per-question progress. body.hint carries that specific
    slot's own current text (a real finding: discarding it and generating a generic JD-grounded
    question produced results with no connection to what HR had actually written for that slot)."""
    job = _get_scoped_job(db, job_id, hr["company_id"])
    question = generate_one_question(
        job.title,
        job.responsibilities,
        job.requirements,
        job.qualifications,
        hint=body.hint,
        existing_questions=body.existing_questions,
    )
    if question is None:
        raise HTTPException(status_code=502, detail="AI gagal membuat pertanyaan. Coba lagi.")
    return GeneratedQuestionOut(question=question)


@router.get("/{job_id}/questions", response_model=list[QuestionOut])
def list_job_questions(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    _get_scoped_job(db, job_id, hr["company_id"])
    questions = repo.interview_questions.list(db, job_id=job_id)
    return sorted(questions, key=lambda q: q.order_index)


@router.put("/{job_id}/questions", response_model=list[QuestionOut])
def update_job_questions(
    job_id: int, body: QuestionsUpdateRequest, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """HR edits/adds/removes draft questions. Only draft-status questions can be edited."""
    job = _get_scoped_job(db, job_id, hr["company_id"])

    existing = {q.id: q for q in repo.interview_questions.list(db, job_id=job_id)}
    for q in existing.values():
        if q.status == "approved":
            raise HTTPException(status_code=400, detail="Cannot edit already-approved questions")

    # Same FK-violation risk as generate_job_questions above: a reopened (draft) question can
    # already have interview_answers pointing at it if a candidate answered it while it was still
    # approved. This always deletes-and-recreates every row, so that would 500 on the DELETE.
    answered = [q for q in existing.values() if repo.interview_answers.list(db, question_id=q.id)]
    if answered:
        raise HTTPException(
            status_code=400,
            detail="Cannot edit — one or more questions already have candidate answers recorded.",
        )

    # Preserve each existing question's own duration_seconds across the delete-and-recreate below
    # — without this, every save would silently reset every question's per-question time limit
    # back to the job default, discarding any PATCH .../duration edits made since the last save.
    durations_by_id = {qid: q.duration_seconds for qid, q in existing.items()}

    for q in existing.values():
        db.delete(q)
    db.commit()

    result = []
    for item in body.questions:
        duration_seconds = durations_by_id.get(
            item.id, item.duration_seconds or _DEFAULT_QUESTION_DURATION_SECONDS
        )
        row = repo.interview_questions.create(
            db,
            job_id=job.id,
            question_text=item.question_text,
            order_index=item.order_index,
            status="draft",
            duration_seconds=duration_seconds,
        )
        result.append(row)
    return result


@router.patch("/{job_id}/questions/{question_id}/duration", response_model=QuestionOut)
def update_question_duration(
    job_id: int,
    question_id: int,
    body: QuestionDurationRequest,
    hr=Depends(get_current_hr),
    db: Session = Depends(get_db),
):
    """Per-question time limit (2026-07-19 follow-up, replacing the earlier job-wide-only design)
    — editable independent of draft/approved status, mirroring the job-level duration PATCH's
    immediate-save pattern. Doesn't touch question_text/order_index/status, so it never needs a
    reopen even on an approved (locked) question."""
    _get_scoped_job(db, job_id, hr["company_id"])
    if body.duration_seconds not in (60, 120, 180):
        raise HTTPException(status_code=400, detail="duration_seconds must be 60, 120, or 180")

    question = repo.interview_questions.get(db, question_id)
    if not question or question.job_id != job_id:
        raise HTTPException(status_code=404, detail="Question not found")

    question.duration_seconds = body.duration_seconds
    db.commit()
    db.refresh(question)
    return question


@router.post("/{job_id}/questions/reopen", response_model=list[QuestionOut])
def reopen_job_questions(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Flips already-approved questions back to draft so HR can add/edit before re-approving."""
    _get_scoped_job(db, job_id, hr["company_id"])

    questions = repo.interview_questions.list(db, job_id=job_id, status="approved")
    for q in questions:
        q.status = "draft"
    db.commit()

    return sorted(repo.interview_questions.list(db, job_id=job_id), key=lambda q: q.order_index)


@router.post("/{job_id}/questions/approve", response_model=list[QuestionOut])
def approve_job_questions(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Flips all draft questions to approved. Candidates only ever see approved questions."""
    _get_scoped_job(db, job_id, hr["company_id"])

    questions = repo.interview_questions.list(db, job_id=job_id, status="draft")
    if not questions:
        raise HTTPException(status_code=400, detail="No draft questions to approve")

    for q in questions:
        q.status = "approved"
    db.commit()

    return repo.interview_questions.list(db, job_id=job_id, status="approved")
