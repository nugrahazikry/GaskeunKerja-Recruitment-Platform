from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.report import build_report

router = APIRouter(prefix="/candidates", tags=["report"])


@router.get("/{candidate_id}/report")
def get_candidate_report(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    job = repo.jobs.get(db, candidate.job_id)
    if not job or job.company_id != hr["company_id"]:
        raise HTTPException(status_code=404, detail="Candidate not found")

    decisions = repo.hr_decisions.list(db, candidate_id=candidate_id)
    if not decisions:
        raise HTTPException(
            status_code=400, detail="Cannot generate report: no HR decision recorded yet"
        )

    return build_report(db, candidate_id, candidate.job_id)
