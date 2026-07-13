from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.rubric_persist import compute_and_persist_interview_summary, score_and_persist_answer

router = APIRouter(prefix="/candidates", tags=["rubric"])


class ScoreOut(BaseModel):
    clarity: int
    relevance: int
    technical_depth: int
    summary: str


class InterviewSummaryOut(BaseModel):
    overall_score: float
    ai_summary_text: str


def _candidate_belongs_to_hr(db: Session, candidate_id: int, company_id: int) -> bool:
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        return False
    job = repo.jobs.get(db, candidate.job_id)
    return bool(job and job.company_id == company_id)


@router.post("/{candidate_id}/answers/{answer_id}/score", response_model=ScoreOut)
def score_candidate_answer(
    candidate_id: int, answer_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    if not _candidate_belongs_to_hr(db, candidate_id, hr["company_id"]):
        raise HTTPException(status_code=404, detail="Candidate not found")

    result = score_and_persist_answer(db, answer_id)
    return ScoreOut(
        clarity=result["clarity"],
        relevance=result["relevance"],
        technical_depth=result["technical_depth"],
        summary=result["summary"],
    )


@router.post("/{candidate_id}/interview-summary", response_model=InterviewSummaryOut)
def build_interview_summary(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    if not _candidate_belongs_to_hr(db, candidate_id, hr["company_id"]):
        raise HTTPException(status_code=404, detail="Candidate not found")

    answers = repo.interview_answers.list(db, candidate_id=candidate_id)
    per_answer_summaries = []
    for answer in answers:
        scored = score_and_persist_answer(db, answer.id)
        per_answer_summaries.append(scored["summary"])

    result = compute_and_persist_interview_summary(db, candidate_id, per_answer_summaries)
    return InterviewSummaryOut(**result)
