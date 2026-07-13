from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr

router = APIRouter(prefix="/decisions", tags=["decisions"])

_VALID_DECISIONS = {"advance", "reject"}


class DecisionRequest(BaseModel):
    candidate_id: int
    decision: str
    notes: str | None = None


class DecisionOut(BaseModel):
    id: int
    candidate_id: int
    decision: str
    decided_by: int

    class Config:
        from_attributes = True


@router.post("", response_model=DecisionOut)
def record_decision(body: DecisionRequest, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Records HR's final pass/reject decision. No code path anywhere finalizes a
    candidate without this endpoint being explicitly called by a human — there is no
    automatic-decision helper, scheduled job, or scoring threshold that writes here."""
    if body.decision not in _VALID_DECISIONS:
        raise HTTPException(status_code=400, detail=f"decision must be one of {_VALID_DECISIONS}")

    candidate = repo.candidates.get(db, body.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    job = repo.jobs.get(db, candidate.job_id)
    if not job or job.company_id != hr["company_id"]:
        raise HTTPException(status_code=404, detail="Candidate not found")

    existing = repo.hr_decisions.list(db, candidate_id=body.candidate_id)
    for row in existing:
        db.delete(row)
    db.commit()

    decision = repo.hr_decisions.create(
        db,
        candidate_id=body.candidate_id,
        decision=body.decision,
        decided_by=int(hr["sub"]),
        notes=body.notes,
    )
    return decision
