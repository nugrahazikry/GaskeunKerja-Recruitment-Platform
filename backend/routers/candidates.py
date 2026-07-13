from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_candidate_by_token, get_current_hr
from services import auth
from services.candidate_ingest import ingest_cv
from services.consent import has_consent, record_consent

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


class CandidateDetailOut(BaseModel):
    """HR-facing candidate detail, used by Area 1 T5c to re-view an existing invite link
    without calling POST /invite again — that endpoint always issues a fresh token, which
    would silently invalidate a link already shared with the candidate mid-demo."""

    id: int
    job_id: int
    alias: str
    invited: bool
    token: str | None
    token_expires_at: str | None


class CandidateSelfOut(BaseModel):
    """Candidate-facing self-info, resolved by token — powers Area 1 T3's route guards
    (expired/invalid token, consent-required redirect) without exposing HR-only fields."""

    id: int
    job_title: str
    has_consent: bool
    has_telegram_link: bool
    interview_completed: bool


class ConsentRequest(BaseModel):
    token: str
    consent_text_version: str


class ConsentOut(BaseModel):
    candidate_id: int
    consent_given: bool


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
    CV-upload time (T5), which was never meant as a real invite link.

    Re-invite-safe (Area 1 T5c): if the candidate was already invited and hasn't
    started the interview yet, calling this again just issues a fresh token/expiry
    without erasing `invited_at` — the Shortlist's 'Belum diundang' status pill is
    keyed off `invited_at`, not the token, so re-opening the invite modal never
    regresses a candidate back to 'not invited'.
    """
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
    if candidate.invited_at is None:
        candidate.invited_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(candidate)

    return InviteOut(
        candidate_id=candidate.id, token=candidate.token, token_expires_at=candidate.token_expires_at.isoformat()
    )


@router.get("/{candidate_id}", response_model=CandidateDetailOut)
def get_candidate_detail(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """HR-facing, read-only. Lets the Shortlist's invite modal re-display an existing
    link (Area 1 T5c) without ever calling POST /invite again just to view it."""
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate or not _job_belongs_to_company(db, candidate.job_id, hr["company_id"]):
        raise HTTPException(status_code=404, detail="Candidate not found")

    invited = candidate.invited_at is not None
    return CandidateDetailOut(
        id=candidate.id,
        job_id=candidate.job_id,
        alias=candidate.alias,
        invited=invited,
        token=candidate.token if invited else None,
        token_expires_at=candidate.token_expires_at.isoformat() if invited else None,
    )


@router.get("/{candidate_id}/self", response_model=CandidateSelfOut)
def get_candidate_self(candidate_id: int, token: str, db: Session = Depends(get_db)):
    """Token-authenticated candidate self-info. A 401 here (invalid/expired token) is what
    Area 1 T3's frontend route guard renders as the shared 'link tidak valid / sudah
    kadaluarsa' screen."""
    candidate = get_candidate_by_token(token, db)
    if candidate.id != candidate_id:
        raise HTTPException(status_code=401, detail="Token does not match this candidate")

    job = repo.jobs.get(db, candidate.job_id)
    answers = repo.interview_answers.list(db, candidate_id=candidate_id)

    return CandidateSelfOut(
        id=candidate.id,
        job_title=job.title if job else "?",
        has_consent=has_consent(db, candidate_id),
        has_telegram_link=candidate.telegram_chat_id is not None,
        interview_completed=len(answers) > 0,
    )


@router.post("/{candidate_id}/consent", response_model=ConsentOut)
def submit_consent(candidate_id: int, body: ConsentRequest, db: Session = Depends(get_db)):
    """Token-authenticated. Records PDP consent before the candidate can start the
    interview (Area 1 T8 gate; enforced server-side already via services.consent in the
    interview-answer submit path)."""
    candidate = get_candidate_by_token(body.token, db)
    if candidate.id != candidate_id:
        raise HTTPException(status_code=401, detail="Token does not match this candidate")

    record_consent(db, candidate_id, body.consent_text_version)
    return ConsentOut(candidate_id=candidate_id, consent_given=True)
