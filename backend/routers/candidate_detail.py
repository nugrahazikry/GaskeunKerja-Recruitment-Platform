from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.delivery import send_decision_notice
from services.education import meets_education
from services.matching import rank_candidates_for_job, rescore_from_existing_skill_gap
from services.skillgap import combine_skills, get_or_compute_skill_gap, persist_skill_gap

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
    summary_text: str | None
    rubric_scores: list[RubricScoreOut]


class KeyStrengthOut(BaseModel):
    title: str
    description: str


class ResumeActionItemOut(BaseModel):
    original: str
    improved: str


class SkillGapOut(BaseModel):
    gap_summary: str
    missing_competencies: list[str]
    matched_competencies: list[str]
    development_priority: str | None
    key_strengths: list[KeyStrengthOut]
    resume_action_items: list[ResumeActionItemOut]
    interview_key_strengths: list[KeyStrengthOut]
    interview_feedback: list[KeyStrengthOut]


class DecisionOut(BaseModel):
    decision: str
    notes: str | None


class ContactEmailIn(BaseModel):
    contact_email: str


class ContactEmailOut(BaseModel):
    candidate_id: int
    contact_email: str | None


class CandidateFullDetailOut(BaseModel):
    candidate_id: int
    alias: str
    job_id: int
    job_title: str
    match_score: float | None
    skills: list[str]
    skills_implicit: list
    experience: list
    qualifications: list
    cv_summary: str | None
    education_history: list
    certifications: list
    featured_projects: list
    organization_experience: list
    skill_gap: SkillGapOut | None
    answers: list[AnswerDetailOut]
    interview_summary_text: str | None
    interview_overall_score: float | None
    decision: DecisionOut | None
    has_telegram_link: bool
    report_sent: bool
    cv_url: str | None
    contact_email: str | None
    has_email: bool
    education_level: str | None
    major: str | None
    meets_education: bool | None
    invited: bool
    invite_email_sent: bool


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
        jd_competencies = repo.jd_competencies.list(db, job_id=job.id, status="active")
        required = [c.competency_name for c in jd_competencies]
        gap = get_or_compute_skill_gap(
            db,
            candidate_id,
            job.id,
            combine_skills(profile.skills, profile.skills_implicit),
            required,
            candidate_experience=profile.experience,
        )
        skill_gap_out = SkillGapOut(**gap)

    answers = repo.interview_answers.list(db, candidate_id=candidate_id)
    questions_by_id = {q.id: q for q in repo.interview_questions.list(db, job_id=job.id)}
    answer_details = []
    for answer in answers:
        transcripts = repo.transcripts.list(db, answer_id=answer.id)
        transcript_text = transcripts[0].transcript_text if transcripts else ""
        summary_text = transcripts[0].summary_text if transcripts else None
        rubric_rows = repo.rubric_scores.list(db, answer_id=answer.id)
        question = questions_by_id.get(answer.question_id)
        answer_details.append(
            AnswerDetailOut(
                answer_id=answer.id,
                question_text=question.question_text if question else "?",
                audio_url=f"/candidates/{candidate_id}/answers/{answer.id}/audio",
                transcript_text=transcript_text,
                summary_text=summary_text,
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

    match_scores = repo.match_scores.list(db, candidate_id=candidate_id, job_id=job.id)
    match_score = match_scores[0].overall_score if match_scores else None

    return CandidateFullDetailOut(
        candidate_id=candidate.id,
        alias=candidate.alias,
        job_id=job.id,
        job_title=job.title,
        match_score=match_score,
        skills=profile.skills if profile else [],
        skills_implicit=(profile.skills_implicit or []) if profile else [],
        experience=profile.experience if profile else [],
        qualifications=profile.qualifications if profile else [],
        cv_summary=profile.cv_summary if profile else None,
        education_history=(profile.education_history or []) if profile else [],
        certifications=(profile.certifications or []) if profile else [],
        featured_projects=(profile.featured_projects or []) if profile else [],
        organization_experience=(profile.organization_experience or []) if profile else [],
        skill_gap=skill_gap_out,
        answers=answer_details,
        interview_summary_text=summary.ai_summary_text if summary else None,
        interview_overall_score=summary.overall_score if summary else None,
        decision=DecisionOut(decision=decision.decision, notes=decision.notes) if decision else None,
        has_telegram_link=candidate.telegram_chat_id is not None,
        report_sent=decision is not None and decision.report_sent_at is not None,
        cv_url=f"/candidates/{candidate_id}/cv" if profile else None,
        contact_email=candidate.contact_email,
        has_email=candidate.contact_email is not None,
        education_level=profile.education_level if profile else None,
        major=profile.major if profile else None,
        meets_education=meets_education(profile.education_level if profile else None, job.required_education_level),
        invited=candidate.invited_at is not None,
        invite_email_sent=candidate.invite_email_sent_at is not None,
    )


@router.post("/{candidate_id}/reanalyze-skill-gap", response_model=SkillGapOut)
def reanalyze_skill_gap(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Manual escape hatch (Round-2 polish, A1's scope guard): skill-gap is normally computed once
    at match time and read from the persisted row. This forces a fresh recompute for the rare case
    a JD's competencies changed after the candidate was already matched — no automatic invalidation
    is built for that case this round (match_scores itself isn't auto-invalidated on JD edit
    either), so this button is the deliberate manual alternative.

    Round-3 follow-up (2026-07-19): the ranking score is now DERIVED from this same skill-gap
    analysis (services/matching.py), so re-analyzing here would otherwise leave match_scores stale
    relative to the freshly recomputed matched/proficiency data — this now also refreshes the
    match score and this job's ranking, not just the skill-gap narrative."""
    candidate, job = _get_scoped_candidate(db, candidate_id, hr["company_id"])

    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    if not profiles:
        raise HTTPException(status_code=400, detail="No parsed CV profile for this candidate yet")

    jd_competencies = repo.jd_competencies.list(db, job_id=job.id, status="active")
    required = [c.competency_name for c in jd_competencies]
    gap = persist_skill_gap(
        db,
        candidate_id,
        job.id,
        combine_skills(profiles[0].skills, profiles[0].skills_implicit),
        required,
        candidate_experience=profiles[0].experience,
    )
    rescore_from_existing_skill_gap(db, candidate_id, job.id)
    rank_candidates_for_job(db, job.id)
    return SkillGapOut(**gap)


@router.patch("/{candidate_id}/contact-email", response_model=ContactEmailOut)
def update_contact_email(
    candidate_id: int, body: ContactEmailIn, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """Round-3 Task 19: contact_email is normally auto-captured from the CV at ingest, but a CV
    without a detectable email (or a wrong extraction) leaves HR needing a manual override."""
    candidate, _ = _get_scoped_candidate(db, candidate_id, hr["company_id"])
    candidate.contact_email = body.contact_email
    db.commit()
    db.refresh(candidate)
    return ContactEmailOut(candidate_id=candidate.id, contact_email=candidate.contact_email)


@router.post("/{candidate_id}/send-decision-notice")
def send_candidate_decision_notice(
    candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """Round-3 Task 19: manual-trigger accept/reject notice email — never automatic on decision,
    to avoid accidental sends while HR is still testing/adjusting a decision."""
    candidate, _ = _get_scoped_candidate(db, candidate_id, hr["company_id"])

    if not candidate.contact_email:
        raise HTTPException(status_code=400, detail="Candidate has no contact_email on file")

    decisions = repo.hr_decisions.list(db, candidate_id=candidate_id)
    if not decisions:
        raise HTTPException(status_code=400, detail="No HR decision recorded yet")

    send_decision_notice(candidate.alias, candidate.contact_email, decisions[0].decision)
    return {"status": "sent", "to": candidate.contact_email, "decision": decisions[0].decision}


@router.get("/{candidate_id}/cv")
def get_candidate_cv(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Streams the candidate's original uploaded CV PDF (Round-3 Task 18) — direct mirror of
    get_answer_audio below. HR-scoped like every other candidate-detail endpoint. The raw PDF
    contains real PII (name/email/phone) by design — this is an HR-facing view, not redacted,
    same as the existing raw_cv_path storage already was."""
    _get_scoped_candidate(db, candidate_id, hr["company_id"])

    profiles = repo.parsed_profiles.list(db, candidate_id=candidate_id)
    if not profiles:
        raise HTTPException(status_code=404, detail="No CV on file for this candidate")

    path = Path(profiles[0].raw_cv_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="CV file not found")

    return FileResponse(path, media_type="application/pdf")


@router.get("/{candidate_id}/answers/{answer_id}/audio")
def get_answer_audio(
    candidate_id: int, answer_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """Streams the stored answer recording for the HR-facing player. HR-scoped like every other
    candidate-detail endpoint — never publicly reachable.

    Round-3 Task 21: recordings are now video+audio webm (camera interview redesign), served as
    video/webm — a browser <video> element plays an audio-only webm from before this change
    just fine (blank frame, working controls), so no branching by candidate/recording age."""
    _get_scoped_candidate(db, candidate_id, hr["company_id"])

    answer = repo.interview_answers.get(db, answer_id)
    if not answer or answer.candidate_id != candidate_id:
        raise HTTPException(status_code=404, detail="Answer not found")

    path = Path(answer.audio_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(path, media_type="video/webm")
