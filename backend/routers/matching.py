from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.matching import compute_match_score, rank_candidates_for_job

router = APIRouter(prefix="/jobs", tags=["matching"])


class MatchOut(BaseModel):
    candidate_id: int
    alias: str
    overall_score: float
    rank: int
    competency_breakdown: dict
    invited: bool
    interview_completed: bool
    decided: bool


@router.get("/{job_id}/candidates", response_model=list[MatchOut])
def get_ranked_candidates(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Status pill derivation (Area 1 T5, resolved 2026-07-12): 'Belum diundang' /
    'Menunggu wawancara' / 'Selesai wawancara' are derived from row presence
    (invited_at, interview_answers, hr_decisions), never a stored status field."""
    job = repo.jobs.get(db, job_id)
    if not job or job.company_id != hr["company_id"]:
        raise HTTPException(status_code=404, detail="Job not found")

    scores = repo.match_scores.list(db, job_id=job_id)
    scores.sort(key=lambda s: s.rank if s.rank else 999999)

    result = []
    for score in scores:
        candidate = repo.candidates.get(db, score.candidate_id)
        answers = repo.interview_answers.list(db, candidate_id=score.candidate_id)
        decisions = repo.hr_decisions.list(db, candidate_id=score.candidate_id)
        result.append(
            MatchOut(
                candidate_id=score.candidate_id,
                alias=candidate.alias if candidate else "?",
                overall_score=score.overall_score,
                rank=score.rank,
                competency_breakdown=score.competency_breakdown,
                invited=bool(candidate and candidate.invited_at is not None),
                interview_completed=len(answers) > 0,
                decided=len(decisions) > 0,
            )
        )
    return result
