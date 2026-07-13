from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_candidate_by_token
from services.consent import ConsentRequiredError
from services.interview_answers import submit_answer

router = APIRouter(prefix="/candidates", tags=["interview_answers"])


class AnswerOut(BaseModel):
    answer_id: int
    audio_path: str
    transcript_text: str


class CandidateQuestionOut(BaseModel):
    id: int
    question_text: str
    order_index: int

    class Config:
        from_attributes = True


@router.get("/{candidate_id}/questions", response_model=list[CandidateQuestionOut])
def list_candidate_questions(candidate_id: int, token: str, db: Session = Depends(get_db)):
    """Candidate-facing (token-authenticated). Only ever returns approved questions —
    candidates never see drafts."""
    candidate = get_candidate_by_token(token, db)
    if candidate.id != candidate_id:
        raise HTTPException(status_code=401, detail="Token does not match this candidate")

    questions = repo.interview_questions.list(db, job_id=candidate.job_id, status="approved")
    return sorted(questions, key=lambda q: q.order_index)


@router.post("/{candidate_id}/answers", response_model=AnswerOut)
async def submit_interview_answer(
    candidate_id: int,
    question_id: int = Form(...),
    session: str = Form(...),
    token: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Candidate-facing (token-authenticated, not HR JWT). Consent-gated: 403 without a
    consent_records row for this candidate."""
    candidate = get_candidate_by_token(token, db)
    if candidate.id != candidate_id:
        raise HTTPException(status_code=401, detail="Token does not match this candidate")

    audio_bytes = await file.read()

    try:
        result = submit_answer(db, candidate_id, question_id, audio_bytes, session)
    except ConsentRequiredError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    return AnswerOut(**result)
