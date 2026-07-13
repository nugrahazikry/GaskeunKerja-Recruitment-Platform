from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.interview_questions import generate_questions

router = APIRouter(prefix="/jobs", tags=["interview_questions"])


class QuestionOut(BaseModel):
    id: int
    job_id: int
    question_text: str
    order_index: int
    status: str

    class Config:
        from_attributes = True


class QuestionUpdateItem(BaseModel):
    id: int | None = None  # None = new question to add
    question_text: str
    order_index: int


class QuestionsUpdateRequest(BaseModel):
    questions: list[QuestionUpdateItem]


def _get_scoped_job(db: Session, job_id: int, company_id: int):
    job = repo.jobs.get(db, job_id)
    if not job or job.company_id != company_id:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/questions/generate", response_model=list[QuestionOut])
def generate_job_questions(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Generates 2-3 draft questions from the JD via Flash. Replaces any existing draft questions."""
    job = _get_scoped_job(db, job_id, hr["company_id"])

    existing = repo.interview_questions.list(db, job_id=job_id, status="draft")
    for q in existing:
        db.delete(q)
    db.commit()

    questions = generate_questions(job.title, job.responsibilities, job.requirements)
    created = []
    for i, q_text in enumerate(questions):
        row = repo.interview_questions.create(
            db, job_id=job_id, question_text=q_text, order_index=i, status="draft"
        )
        created.append(row)
    return created


@router.get("/{job_id}/questions", response_model=list[QuestionOut])
def list_job_questions(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    _get_scoped_job(db, job_id, hr["company_id"])
    questions = repo.interview_questions.list(db, job_id=job_id)
    return sorted(questions, key=lambda q: q.order_index)


@router.put("/{job_id}/questions", response_model=list[QuestionOut])
def update_job_questions(
    job_id: int, body: QuestionsUpdateRequest, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """HR edits/adds/removes draft questions. Only draft-status questions can be edited."""
    job = _get_scoped_job(db, job_id, hr["company_id"])

    existing = {q.id: q for q in repo.interview_questions.list(db, job_id=job_id)}
    for q in existing.values():
        if q.status == "approved":
            raise HTTPException(status_code=400, detail="Cannot edit already-approved questions")

    for q in existing.values():
        db.delete(q)
    db.commit()

    result = []
    for item in body.questions:
        row = repo.interview_questions.create(
            db, job_id=job.id, question_text=item.question_text, order_index=item.order_index, status="draft"
        )
        result.append(row)
    return result


@router.post("/{job_id}/questions/approve", response_model=list[QuestionOut])
def approve_job_questions(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Flips all draft questions to approved. Candidates only ever see approved questions."""
    _get_scoped_job(db, job_id, hr["company_id"])

    questions = repo.interview_questions.list(db, job_id=job_id, status="draft")
    if not questions:
        raise HTTPException(status_code=400, detail="No draft questions to approve")

    for q in questions:
        q.status = "approved"
    db.commit()

    return repo.interview_questions.list(db, job_id=job_id, status="approved")
