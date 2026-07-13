from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.delivery import NoTelegramLinkError, send_report
from services.report import build_report

router = APIRouter(prefix="/candidates", tags=["report"])


def _get_scoped_candidate(db: Session, candidate_id: int, company_id: int):
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    job = repo.jobs.get(db, candidate.job_id)
    if not job or job.company_id != company_id:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


def _require_decision(db: Session, candidate_id: int):
    decisions = repo.hr_decisions.list(db, candidate_id=candidate_id)
    if not decisions:
        raise HTTPException(
            status_code=400, detail="Cannot generate report: no HR decision recorded yet"
        )


@router.get("/{candidate_id}/report")
def get_candidate_report(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    candidate = _get_scoped_candidate(db, candidate_id, hr["company_id"])
    _require_decision(db, candidate_id)
    return build_report(db, candidate_id, candidate.job_id)


@router.post("/{candidate_id}/send-report")
def send_candidate_report(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """HR triggers delivery with one click — PDF + summary auto-sent via Telegram."""
    _get_scoped_candidate(db, candidate_id, hr["company_id"])
    _require_decision(db, candidate_id)

    try:
        result = send_report(db, candidate_id)
    except NoTelegramLinkError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return {"status": "sent", **result}
