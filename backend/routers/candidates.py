from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services import auth
from services.candidate_ingest import ingest_cv

router = APIRouter(prefix="/candidates", tags=["candidates"])


class CandidateOut(BaseModel):
    id: int
    job_id: int
    alias: str

    class Config:
        from_attributes = True


def _job_belongs_to_company(db: Session, job_id: int, company_id: int) -> bool:
    job = repo.jobs.get(db, job_id)
    return bool(job and job.company_id == company_id)


@router.post("", response_model=CandidateOut)
async def create_candidate(
    job_id: int = Form(...),
    alias: str = Form(...),
    file: UploadFile = File(...),
    hr=Depends(get_current_hr),
    db: Session = Depends(get_db),
):
    """HR/seed-side only for MVP — not a public candidate-facing endpoint (see Area 1 T8 note)."""
    if not _job_belongs_to_company(db, job_id, hr["company_id"]):
        raise HTTPException(status_code=404, detail="Job not found")

    token, expires_at = auth.generate_candidate_token()
    candidate = repo.candidates.create(
        db, job_id=job_id, alias=alias, token=token, token_expires_at=expires_at
    )

    file_bytes = await file.read()
    ingest_cv(db, candidate.id, file_bytes, alias=alias)

    return candidate
