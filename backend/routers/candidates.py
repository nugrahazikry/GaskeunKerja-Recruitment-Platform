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


class InviteOut(BaseModel):
    candidate_id: int
    token: str
    token_expires_at: str


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


@router.post("/{candidate_id}/invite", response_model=InviteOut)
def invite_candidate(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Generates a fresh, meaningful invite token — only callable once the job's
    interview questions are approved (T9b). Regenerates the placeholder token set at
    CV-upload time (T5), which was never meant as a real invite link."""
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate or not _job_belongs_to_company(db, candidate.job_id, hr["company_id"]):
        raise HTTPException(status_code=404, detail="Candidate not found")

    approved_questions = repo.interview_questions.list(db, job_id=candidate.job_id, status="approved")
    if not approved_questions:
        raise HTTPException(
            status_code=400, detail="Cannot invite: interview questions are not approved yet"
        )

    token, expires_at = auth.generate_candidate_token()
    candidate.token = token
    candidate.token_expires_at = expires_at
    db.commit()
    db.refresh(candidate)

    return InviteOut(
        candidate_id=candidate.id, token=candidate.token, token_expires_at=candidate.token_expires_at.isoformat()
    )
