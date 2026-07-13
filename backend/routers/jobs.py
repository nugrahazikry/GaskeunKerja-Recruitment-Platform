from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services import extract

router = APIRouter(prefix="/jobs", tags=["jobs"])


class JobCreateRequest(BaseModel):
    title: str
    responsibilities: str
    requirements: str
    qualifications: str


class JobUpdateRequest(BaseModel):
    title: str
    responsibilities: str
    requirements: str
    qualifications: str


class CompetencyOut(BaseModel):
    id: int
    competency_name: str
    importance_level: float

    class Config:
        from_attributes = True


class JobOut(BaseModel):
    id: int
    company_id: int
    title: str
    responsibilities: str
    requirements: str
    qualifications: str
    status: str

    class Config:
        from_attributes = True


def _extract_and_store_competencies(db: Session, job) -> None:
    existing = repo.jd_competencies.list(db, job_id=job.id)
    for row in existing:
        db.delete(row)
    db.commit()

    competencies = extract.extract_competencies(
        job.title, job.responsibilities, job.requirements, job.qualifications
    )
    for c in competencies:
        repo.jd_competencies.create(
            db, job_id=job.id, competency_name=c["competency_name"], importance_level=c["importance_level"]
        )


@router.post("", response_model=JobOut)
def create_job(body: JobCreateRequest, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    job = repo.jobs.create(
        db,
        company_id=hr["company_id"],
        title=body.title,
        responsibilities=body.responsibilities,
        requirements=body.requirements,
        qualifications=body.qualifications,
        status="active",
    )
    _extract_and_store_competencies(db, job)
    return job


@router.get("", response_model=list[JobOut])
def list_jobs(hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    return repo.jobs.list(db, company_id=hr["company_id"])


def _get_scoped_job(db: Session, job_id: int, company_id: int):
    job = repo.jobs.get(db, job_id)
    if not job or job.company_id != company_id:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    return _get_scoped_job(db, job_id, hr["company_id"])


@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int, body: JobUpdateRequest, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    job = _get_scoped_job(db, job_id, hr["company_id"])
    job.title = body.title
    job.responsibilities = body.responsibilities
    job.requirements = body.requirements
    job.qualifications = body.qualifications
    db.commit()
    db.refresh(job)
    _extract_and_store_competencies(db, job)
    return job


@router.delete("/{job_id}", response_model=JobOut)
def close_job(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Soft-delete: sets status='closed'. Never a real SQL DELETE — avoids FK errors
    against candidates/interviews/audit_log and preserves audit history."""
    job = _get_scoped_job(db, job_id, hr["company_id"])
    job.status = "closed"
    db.commit()
    db.refresh(job)
    return job


@router.get("/{job_id}/competencies", response_model=list[CompetencyOut])
def get_job_competencies(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    _get_scoped_job(db, job_id, hr["company_id"])
    return repo.jd_competencies.list(db, job_id=job_id)
