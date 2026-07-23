from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class PerJobStat(BaseModel):
    job_id: int
    title: str
    status: str
    candidate_count: int
    interviewed_count: int
    decided_count: int


class AttentionItem(BaseModel):
    type: str  # "undecided" | "no_approved_questions" | "report_not_sent"
    label: str
    job_id: int | None = None
    candidate_id: int | None = None


class ScoreDistribution(BaseModel):
    bucket_0_40: int
    bucket_40_60: int
    bucket_60_80: int
    bucket_80_100: int


class JobConversion(BaseModel):
    job_id: int
    title: str
    invited_count: int
    completed_count: int


class CompetencyGap(BaseModel):
    competency_name: str
    missing_pct: float


class JobDecisionBreakdown(BaseModel):
    job_id: int
    title: str
    advance_count: int
    reject_count: int
    pending_count: int  # interviewed, no decision yet


class DashboardStatsOut(BaseModel):
    company_name: str
    active_jobs: int
    closed_jobs: int
    total_candidates: int
    # Pipeline stages — derived from row presence, matching matching.py's authoritative
    # semantics (invited_at + interview_answers presence), never a stored status field.
    belum_diundang: int
    menunggu_wawancara: int
    selesai_wawancara: int
    decisions_advance: int
    decisions_reject: int
    decisions_pending: int  # interviewed but no decision yet
    reports_sent: int
    avg_match_score: float | None
    per_job: list[PerJobStat]
    attention: list[AttentionItem]
    score_distribution: ScoreDistribution
    conversion_by_job: list[JobConversion]
    competency_gaps: list[CompetencyGap]  # top gaps for the job with the most candidates
    decisions_by_job: list[JobDecisionBreakdown]


_ATTENTION_CAP = 8


@router.get("/stats", response_model=DashboardStatsOut)
def get_dashboard_stats(hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Company-scoped recruitment overview aggregated in Python (the generic repository
    only supports equality-filter list queries — no COUNT/GROUP BY). Pipeline-stage
    derivation follows the same row-presence rules as routers/matching.py."""
    company_id = hr["company_id"]
    company = repo.companies.get(db, company_id)
    company_name = company.name if company else ""

    jobs = repo.jobs.list(db, company_id=company_id)
    active_jobs = sum(1 for j in jobs if j.status == "active")
    closed_jobs = sum(1 for j in jobs if j.status == "closed")

    total_candidates = 0
    belum_diundang = 0
    menunggu_wawancara = 0
    selesai_wawancara = 0
    decisions_advance = 0
    decisions_reject = 0
    decisions_pending = 0
    reports_sent = 0
    match_score_sum = 0.0
    match_score_count = 0

    per_job: list[PerJobStat] = []
    attention: list[AttentionItem] = []
    conversion_by_job: list[JobConversion] = []
    decisions_by_job: list[JobDecisionBreakdown] = []
    score_buckets = {"0_40": 0, "40_60": 0, "60_80": 0, "80_100": 0}
    largest_job_id: int | None = None
    largest_job_candidate_count = -1

    for job in jobs:
        candidates = repo.candidates.list(db, job_id=job.id)
        approved_questions = repo.interview_questions.list(db, job_id=job.id, status="approved")

        job_candidate_count = len(candidates)
        job_interviewed = 0
        job_decided = 0
        job_invited = 0
        job_completed = 0
        job_advance = 0
        job_reject = 0
        job_pending = 0

        total_candidates += job_candidate_count
        if job_candidate_count > largest_job_candidate_count:
            largest_job_candidate_count = job_candidate_count
            largest_job_id = job.id

        # Active job that can't actually invite anyone yet — a real blocker worth surfacing.
        if job.status == "active" and job_candidate_count > 0 and not approved_questions:
            if len(attention) < _ATTENTION_CAP:
                attention.append(
                    AttentionItem(
                        type="no_approved_questions",
                        label=f"Lowongan \"{job.title}\" belum punya pertanyaan disetujui — kandidat belum bisa diundang.",
                        job_id=job.id,
                    )
                )

        for candidate in candidates:
            answers = repo.interview_answers.list(db, candidate_id=candidate.id)
            decisions = repo.hr_decisions.list(db, candidate_id=candidate.id)
            match_scores = repo.match_scores.list(db, candidate_id=candidate.id, job_id=job.id)

            interviewed = len(answers) > 0

            if candidate.invited_at is None:
                belum_diundang += 1
            elif not interviewed:
                menunggu_wawancara += 1
            else:
                selesai_wawancara += 1

            if interviewed:
                job_interviewed += 1

            if candidate.invited_at is not None:
                job_invited += 1
                if interviewed:
                    job_completed += 1

            if match_scores:
                score = match_scores[0].overall_score
                match_score_sum += score
                match_score_count += 1
                pct = score * 100
                if pct < 40:
                    score_buckets["0_40"] += 1
                elif pct < 60:
                    score_buckets["40_60"] += 1
                elif pct < 80:
                    score_buckets["60_80"] += 1
                else:
                    score_buckets["80_100"] += 1

            if decisions:
                job_decided += 1
                decision = decisions[0]
                if decision.decision == "advance":
                    decisions_advance += 1
                    job_advance += 1
                elif decision.decision == "reject":
                    decisions_reject += 1
                    job_reject += 1
                if decision.report_sent_at is not None:
                    reports_sent += 1
                elif len(attention) < _ATTENTION_CAP:
                    attention.append(
                        AttentionItem(
                            type="report_not_sent",
                            label=f"Kandidat {candidate.alias} sudah diputuskan tapi laporan belum dikirim.",
                            job_id=job.id,
                            candidate_id=candidate.id,
                        )
                    )
            elif interviewed:
                # Interviewed but no decision — the recruiter's most direct next action.
                decisions_pending += 1
                job_pending += 1
                if len(attention) < _ATTENTION_CAP:
                    attention.append(
                        AttentionItem(
                            type="undecided",
                            label=f"Kandidat {candidate.alias} sudah selesai wawancara tapi belum ada keputusan.",
                            job_id=job.id,
                            candidate_id=candidate.id,
                        )
                    )

        per_job.append(
            PerJobStat(
                job_id=job.id,
                title=job.title,
                status=job.status,
                candidate_count=job_candidate_count,
                interviewed_count=job_interviewed,
                decided_count=job_decided,
            )
        )
        if job_invited > 0:
            conversion_by_job.append(
                JobConversion(
                    job_id=job.id, title=job.title, invited_count=job_invited, completed_count=job_completed
                )
            )
        if job_advance or job_reject or job_pending:
            decisions_by_job.append(
                JobDecisionBreakdown(
                    job_id=job.id,
                    title=job.title,
                    advance_count=job_advance,
                    reject_count=job_reject,
                    pending_count=job_pending,
                )
            )

    avg_match_score = (match_score_sum / match_score_count) if match_score_count else None

    competency_gaps: list[CompetencyGap] = []
    if largest_job_id is not None and largest_job_candidate_count > 0:
        required = repo.jd_competencies.list(db, job_id=largest_job_id, status="active")
        job_scores = repo.match_scores.list(db, job_id=largest_job_id)
        candidate_pool = len(job_scores)
        if candidate_pool > 0:
            for comp in required:
                name_lower = comp.competency_name.strip().lower()
                matched = sum(
                    1
                    for s in job_scores
                    if name_lower in {
                        m.strip().lower() for m in s.competency_breakdown.get("matched_competencies", [])
                    }
                )
                missing_pct = (candidate_pool - matched) / candidate_pool * 100
                competency_gaps.append(
                    CompetencyGap(competency_name=comp.competency_name, missing_pct=missing_pct)
                )
            competency_gaps.sort(key=lambda g: g.missing_pct, reverse=True)
            competency_gaps = competency_gaps[:7]

    return DashboardStatsOut(
        company_name=company_name,
        active_jobs=active_jobs,
        closed_jobs=closed_jobs,
        total_candidates=total_candidates,
        belum_diundang=belum_diundang,
        menunggu_wawancara=menunggu_wawancara,
        selesai_wawancara=selesai_wawancara,
        decisions_advance=decisions_advance,
        decisions_reject=decisions_reject,
        decisions_pending=decisions_pending,
        reports_sent=reports_sent,
        avg_match_score=avg_match_score,
        per_job=per_job,
        attention=attention,
        score_distribution=ScoreDistribution(
            bucket_0_40=score_buckets["0_40"],
            bucket_40_60=score_buckets["40_60"],
            bucket_60_80=score_buckets["60_80"],
            bucket_80_100=score_buckets["80_100"],
        ),
        conversion_by_job=conversion_by_job,
        competency_gaps=competency_gaps,
        decisions_by_job=decisions_by_job,
    )
