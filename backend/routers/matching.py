from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.education import meets_education
from services.matching import compute_match_score, rank_candidates_for_job

router = APIRouter(prefix="/jobs", tags=["matching"])


class CompetencyStatus(BaseModel):
    competency_name: str
    matched: bool
    # 1-3, only present when matched=True — how strongly the candidate's experience evidences
    # this competency (services/skillgap.py::rate_competency_proficiency). None when not matched.
    proficiency: int | None


class MatchOut(BaseModel):
    candidate_id: int
    alias: str
    overall_score: float
    rank: int
    competency_breakdown: dict
    competency_status: list[CompetencyStatus]
    latest_role: str | None
    invited: bool
    interview_completed: bool
    decided: bool
    cv_url: str | None
    education_level: str | None
    major: str | None
    meets_education: bool | None
    has_email: bool
    # Round 14 (real bug, user-reported): the ONLY real signal that an invite email was actually
    # sent (routers/candidates.py::send_candidate_invite_email) — invited_at/has_email are NOT
    # proof of a real invite (invited_at is set just from opening the invite modal, and has_email
    # can flip true long after with no send action happening). "Menunggu Wawancara" is gated on
    # this now, not invited_at.
    invite_email_sent: bool
    # Round-3 follow-up (2026-07-19): user-visible signal for point #12's known first-view latency
    # — skill_gap_results is computed lazily per-candidate on first view (not bulk-backfilled by
    # default, a deliberate choice), so HR can see up front which candidates will load instantly
    # vs. which will take ~30s the first time they're opened.
    skill_gap_ready: bool


@router.get("/{job_id}/candidates", response_model=list[MatchOut])
def get_ranked_candidates(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Status pill derivation (Area 1 T5, resolved 2026-07-12): 'Belum diundang' /
    'Menunggu wawancara' / 'Selesai wawancara' are derived from row presence
    (invited_at, interview_answers, hr_decisions), never a stored status field."""
    job = repo.jobs.get(db, job_id)
    if not job or job.company_id != hr["company_id"]:
        raise HTTPException(status_code=404, detail="Job not found")

    required_competencies = repo.jd_competencies.list(db, job_id=job_id, status="active")

    scores = repo.match_scores.list(db, job_id=job_id)
    scores.sort(key=lambda s: s.rank if s.rank else 999999)

    result = []
    for score in scores:
        candidate = repo.candidates.get(db, score.candidate_id)
        answers = repo.interview_answers.list(db, candidate_id=score.candidate_id)
        decisions = repo.hr_decisions.list(db, candidate_id=score.candidate_id)

        matched_names = {
            name.strip().lower() for name in score.competency_breakdown.get("matched_competencies", [])
        }
        proficiency_by_name = {
            name.strip().lower(): value
            for name, value in score.competency_breakdown.get("competency_proficiency", {}).items()
        }
        competency_status = [
            CompetencyStatus(
                competency_name=jc.competency_name,
                matched=jc.competency_name.strip().lower() in matched_names,
                proficiency=proficiency_by_name.get(jc.competency_name.strip().lower()),
            )
            for jc in required_competencies
        ]

        profiles = repo.parsed_profiles.list(db, candidate_id=score.candidate_id)
        latest_role = None
        if profiles and profiles[0].experience:
            first = profiles[0].experience[0]
            if isinstance(first, dict):
                latest_role = first.get("role")

        education_level = profiles[0].education_level if profiles else None
        major = profiles[0].major if profiles else None
        skill_gap_ready = len(
            repo.skill_gap_results.list(db, candidate_id=score.candidate_id, job_id=job_id)
        ) > 0

        result.append(
            MatchOut(
                candidate_id=score.candidate_id,
                alias=candidate.alias if candidate else "?",
                overall_score=score.overall_score,
                rank=score.rank,
                competency_breakdown=score.competency_breakdown,
                competency_status=competency_status,
                latest_role=latest_role,
                invited=bool(candidate and candidate.invited_at is not None),
                interview_completed=len(answers) > 0,
                decided=len(decisions) > 0,
                cv_url=f"/candidates/{score.candidate_id}/cv" if profiles else None,
                education_level=education_level,
                major=major,
                meets_education=meets_education(education_level, job.required_education_level),
                has_email=bool(candidate and candidate.contact_email),
                invite_email_sent=bool(candidate and candidate.invite_email_sent_at is not None),
                skill_gap_ready=skill_gap_ready,
            )
        )
    return result
