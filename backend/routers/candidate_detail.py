from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.skillgap import analyze_skill_gap

router = APIRouter(prefix="/candidates", tags=["candidate_detail"])


class RubricScoreOut(BaseModel):
    criterion_name: str
    score: int
    rationale: str


class AnswerDetailOut(BaseModel):
    answer_id: int
    question_text: str
    audio_url: str
    transcript_text: str
    rubric_scores: list[RubricScoreOut]


class SkillGapOut(BaseModel):
    gap_summary: str
    missing_competencies: list[str]
    development_priority: str | None


class DecisionOut(BaseModel):
    decision: str
    notes: str | None


class CandidateFullDetailOut(BaseModel):
    candidate_id: int
    alias: str
    job_id: int
    job_title: str
    skills: list[str]
    experience: list
    qualifications: list
    skill_gap: SkillGapOut | None
    answers: list[AnswerDetailOut]
    interview_summary_text: str | None
    interview_overall_score: float | None
    decision: DecisionOut | None
    has_telegram_link: bool
    report_sent: bool


def _get_scoped_candidate(db: Session, candidate_id: int, company_id: int):
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    job = repo.jobs.get(db, candidate.job_id)
    if not job or job.company_id != company_id:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate, job


@router.get("/{candidate_id}/detail", response_model=CandidateFullDetailOut)
def get_candidate_full_detail(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """HR-facing candidate detail screen (Area 1 T7): parsed CV + skill-gap, per-answer
    audio/transcript/rubric, interview summary, decision status, report/Telegram state —
    everything the decision + report-delivery screen needs in one call."""
    candidate, job = _get_scoped_candidate(db, candidate_id, hr["company_id"])

    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    profile = profiles[0] if profiles else None

    skill_gap_out = None
    if profile:
        jd_competencies = repo.jd_competencies.list(db, job_id=job.id)
        required = [c.competency_name for c in jd_competencies]
        gap = analyze_skill_gap(profile.skills, required)
        skill_gap_out = SkillGapOut(**gap)

    answers = repo.interview_answers.list(db, candidate_id=candidate_id)
    questions_by_id = {q.id: q for q in repo.interview_questions.list(db, job_id=job.id)}
    answer_details = []
    for answer in answers:
        transcripts = repo.transcripts.list(db, answer_id=answer.id)
        transcript_text = transcripts[0].transcript_text if transcripts else ""
        rubric_rows = repo.rubric_scores.list(db, answer_id=answer.id)
        question = questions_by_id.get(answer.question_id)
        answer_details.append(
            AnswerDetailOut(
                answer_id=answer.id,
                question_text=question.question_text if question else "?",
                audio_url=f"/candidates/{candidate_id}/answers/{answer.id}/audio",
                transcript_text=transcript_text,
                rubric_scores=[
                    RubricScoreOut(criterion_name=r.criterion_name, score=r.score, rationale=r.rationale)
                    for r in rubric_rows
                ],
            )
        )

    summaries = repo.interview_summaries.list(db, candidate_id=candidate_id)
    summary = summaries[0] if summaries else None

    decisions = repo.hr_decisions.list(db, candidate_id=candidate_id)
    decision = decisions[0] if decisions else None

    return CandidateFullDetailOut(
        candidate_id=candidate.id,
        alias=candidate.alias,
        job_id=job.id,
        job_title=job.title,
        skills=profile.skills if profile else [],
        experience=profile.experience if profile else [],
        qualifications=profile.qualifications if profile else [],
        skill_gap=skill_gap_out,
        answers=answer_details,
        interview_summary_text=summary.ai_summary_text if summary else None,
        interview_overall_score=summary.overall_score if summary else None,
        decision=DecisionOut(decision=decision.decision, notes=decision.notes) if decision else None,
        has_telegram_link=candidate.telegram_chat_id is not None,
        report_sent=decision is not None and decision.report_sent_at is not None,
    )


@router.get("/{candidate_id}/answers/{answer_id}/audio")
def get_answer_audio(
    candidate_id: int, answer_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """Streams the stored answer audio file for the HR-facing player. HR-scoped like
    every other candidate-detail endpoint — never publicly reachable."""
    _get_scoped_candidate(db, candidate_id, hr["company_id"])

    answer = repo.interview_answers.get(db, answer_id)
    if not answer or answer.candidate_id != candidate_id:
        raise HTTPException(status_code=404, detail="Answer not found")

    path = Path(answer.audio_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(path, media_type="audio/webm")
