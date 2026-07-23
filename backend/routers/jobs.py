import logging
import shutil
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import STORAGE_DIR
from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services import extract
from services.job_folders import ensure_job_folder

router = APIRouter(prefix="/jobs", tags=["jobs"])
logger = logging.getLogger("gaskeun")


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
    status: str
    source: str  # "ai" | "custom" — only "ai"+"dismissed" rows surface in the recommended pool

    class Config:
        from_attributes = True


class CompetencyAddRequest(BaseModel):
    competency_name: str
    importance_level: float = 1.0


class JobReportListItemOut(BaseModel):
    candidate_id: int
    alias: str
    interview_completed: bool
    # 2026-07-22 (user-reported real bug/"glitch"): interview_completed only means the video
    # answers exist — it says nothing about whether the post-interview LLM chain (transcription
    # scoring, summary, recommendation extras, and finally the upskilling plan) has actually
    # finished. Without this, "Lihat Laporan" was clickable the instant the interview ended, and
    # candidates caught mid-pipeline showed a report with a null/empty upskilling_plan section as
    # if it were final. True only once skill_gap_results.upskilling_plan is populated — the last
    # field update_recommendation_extras_after_interview() writes, success or graceful fallback.
    processing_complete: bool
    decision: str | None
    decided_at: str | None
    match_score: float | None
    report_sent: bool


class JobOut(BaseModel):
    id: int
    company_id: int
    company_name: str
    title: str
    responsibilities: str
    requirements: str
    qualifications: str
    required_education_level: str | None
    required_major: str | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class JobListItemOut(JobOut):
    candidate_count: int
    question_status: str  # "none" | "draft" | "approved"
    # Pipeline-stage breakdown for this job — same row-presence derivation rules as
    # routers/dashboard.py's company-wide funnel (invited_at / interview_answers / hr_decisions
    # presence), just scoped to one job instead of aggregated across all of them. Powers the
    # "Alur Kandidat" stacked bar on the Lowongan list page (point #5, Round-2 polish).
    belum_diundang: int
    menunggu_wawancara: int
    selesai_wawancara: int
    diputuskan: int


def _to_job_out(job, company_name: str) -> JobOut:
    return JobOut(
        id=job.id,
        company_id=job.company_id,
        company_name=company_name,
        title=job.title,
        responsibilities=job.responsibilities,
        requirements=job.requirements,
        qualifications=job.qualifications,
        required_education_level=job.required_education_level,
        required_major=job.required_major,
        status=job.status,
        created_at=job.created_at,
    )


def _question_status(db: Session, job_id: int) -> str:
    questions = repo.interview_questions.list(db, job_id=job_id)
    if not questions:
        return "none"
    if any(q.status == "approved" for q in questions):
        return "approved"
    return "draft"


def _pipeline_breakdown(db: Session, job_id: int) -> dict:
    """Same derivation rules as routers/dashboard.py's company-wide funnel, scoped to one job."""
    belum_diundang = 0
    menunggu_wawancara = 0
    selesai_wawancara = 0
    diputuskan = 0
    for candidate in repo.candidates.list(db, job_id=job_id):
        interviewed = len(repo.interview_answers.list(db, candidate_id=candidate.id)) > 0
        if candidate.invited_at is None:
            belum_diundang += 1
        elif not interviewed:
            menunggu_wawancara += 1
        else:
            selesai_wawancara += 1
        if repo.hr_decisions.list(db, candidate_id=candidate.id):
            diputuskan += 1
    return {
        "belum_diundang": belum_diundang,
        "menunggu_wawancara": menunggu_wawancara,
        "selesai_wawancara": selesai_wawancara,
        "diputuskan": diputuskan,
    }


def _to_job_list_item(db: Session, job, company_name: str) -> JobListItemOut:
    return JobListItemOut(
        **_to_job_out(job, company_name).model_dump(),
        candidate_count=len(repo.match_scores.list(db, job_id=job.id)),
        question_status=_question_status(db, job.id),
        **_pipeline_breakdown(db, job.id),
    )


def _extract_and_store_competencies(db: Session, job) -> None:
    """Replaces only the ACTIVE, AI-SOURCED competency set — dismissed rows (the "recommended
    pool", A2) AND any HR-added custom competency (active or dismissed) are deliberately left
    untouched, so re-extracting on a JD edit never wipes out something the HR explicitly reviewed,
    dismissed, or typed in themselves.

    Real bug found + fixed same day: re-extraction only deleted active+ai rows before inserting
    fresh ones, but never checked whether a competency by that name already existed elsewhere
    (e.g. dismissed) — so re-saving the same JD text could recreate an active row for a name the
    HR had just dismissed, showing the same competency duplicated in both the active list and the
    recommended pool simultaneously. Now skips creating a competency whose name already exists
    for this job in ANY status, so a dismissal is never silently overridden by a re-extraction."""
    existing = repo.jd_competencies.list(db, job_id=job.id, status="active", source="ai")
    for row in existing:
        db.delete(row)
    db.commit()

    remaining_names = {
        row.competency_name.strip().lower() for row in repo.jd_competencies.list(db, job_id=job.id)
    }

    competencies = extract.extract_competencies(
        job.title, job.responsibilities, job.requirements, job.qualifications
    )
    for c in competencies:
        name_key = c["competency_name"].strip().lower()
        if name_key in remaining_names:
            continue
        repo.jd_competencies.create(
            db,
            job_id=job.id,
            competency_name=c["competency_name"],
            importance_level=c["importance_level"],
            status="active",
            source="ai",
        )
        remaining_names.add(name_key)

    education = extract.extract_education_requirement(job.qualifications)
    job.required_education_level = education["required_education_level"]
    job.required_major = education["required_major"]
    db.commit()


def _get_company_name(db: Session, company_id: int) -> str:
    company = repo.companies.get(db, company_id)
    return company.name if company else ""


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
    ensure_job_folder(job.id, job.title)
    return _to_job_out(job, _get_company_name(db, hr["company_id"]))


@router.get("", response_model=list[JobListItemOut])
def list_jobs(hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    company_name = _get_company_name(db, hr["company_id"])
    jobs = repo.jobs.list(db, company_id=hr["company_id"])
    return [_to_job_list_item(db, job, company_name) for job in jobs]


def _get_scoped_job(db: Session, job_id: int, company_id: int):
    job = repo.jobs.get(db, job_id)
    if not job or job.company_id != company_id:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    job = _get_scoped_job(db, job_id, hr["company_id"])
    return _to_job_out(job, _get_company_name(db, hr["company_id"]))


@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int, body: JobUpdateRequest, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """Round-3 follow-up #9 (2026-07-19): editing an existing job's text fields no longer
    re-extracts/re-stores competencies at all (previously called _extract_and_store_competencies
    here, same as create_job). Real problem this closes: skill-gap analysis for already-scored
    candidates is computed against a job's competency list at analysis time — if HR could freely
    edit that list afterward (this endpoint used to reopen the full add/dismiss/restore review
    modal on every edit save too, see JobsListPage.tsx), every existing candidate's skill-gap/score
    would silently go stale relative to the new list, with no auto-invalidation mechanism to catch
    up (a known, previously-documented gap — see T17-followup's stale-competency-list note).
    Competencies are now a one-time decision made at CREATE time only (create_job, unchanged) —
    editing a job's description afterward is purely a text update."""
    job = _get_scoped_job(db, job_id, hr["company_id"])
    job.title = body.title
    job.responsibilities = body.responsibilities
    job.requirements = body.requirements
    job.qualifications = body.qualifications
    db.commit()
    db.refresh(job)
    return _to_job_out(job, _get_company_name(db, hr["company_id"]))


@router.delete("/{job_id}", response_model=JobOut)
def close_job(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Soft-delete: sets status='closed'. Never a real SQL DELETE — avoids FK errors
    against candidates/interviews/audit_log and preserves audit history."""
    job = _get_scoped_job(db, job_id, hr["company_id"])
    job.status = "closed"
    db.commit()
    db.refresh(job)
    return _to_job_out(job, _get_company_name(db, hr["company_id"]))


@router.delete("/{job_id}/permanent")
def hard_delete_job(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Real, irreversible cascade delete — separate from the existing soft-close DELETE above
    (kept as-is). Round-2 polish (2026-07-17), user-confirmed tradeoff: this destroys audit
    history for the job. No ORM cascade exists anywhere in this schema (confirmed by reading
    every model file), so the cascade is hand-written here in FK-safe order, plus on-disk
    CV/audio/report file cleanup per candidate."""
    job = _get_scoped_job(db, job_id, hr["company_id"])

    candidates = repo.candidates.list(db, job_id=job_id)
    candidate_ids = [c.id for c in candidates]

    for candidate_id in candidate_ids:
        for answer in repo.interview_answers.list(db, candidate_id=candidate_id):
            for row in repo.rubric_scores.list(db, answer_id=answer.id):
                db.delete(row)
            for row in repo.transcripts.list(db, answer_id=answer.id):
                db.delete(row)
            db.delete(answer)
        for row in repo.interview_summaries.list(db, candidate_id=candidate_id):
            db.delete(row)
        for row in repo.hr_decisions.list(db, candidate_id=candidate_id):
            db.delete(row)
        for row in repo.consent_records.list(db, candidate_id=candidate_id):
            db.delete(row)
        for row in repo.match_scores.list(db, candidate_id=candidate_id, job_id=job_id):
            db.delete(row)
        for row in repo.skill_gap_results.list(db, candidate_id=candidate_id, job_id=job_id):
            db.delete(row)
        for row in repo.parsed_profiles.list(db, candidate_id=candidate_id):
            db.delete(row)
    db.commit()

    for row in repo.interview_questions.list(db, job_id=job_id):
        db.delete(row)
    for row in repo.jd_competencies.list(db, job_id=job_id):
        db.delete(row)
    db.commit()

    # Best-effort audit_log cleanup: entity_type/entity_id are free-form (no FK constraint), so
    # this matches the two conventions actually used ("job", "candidate") rather than being a
    # guaranteed-exhaustive cascade — acceptable given the user explicitly accepted losing audit
    # history for a real hard-delete.
    for row in repo.audit_log.list(db, entity_type="job", entity_id=job_id):
        db.delete(row)
    for candidate_id in candidate_ids:
        for row in repo.audit_log.list(db, entity_type="candidate", entity_id=candidate_id):
            db.delete(row)
    db.commit()

    for candidate_id in candidate_ids:
        db.delete(repo.candidates.get(db, candidate_id))
    db.commit()

    db.delete(job)
    db.commit()

    for candidate_id in candidate_ids:
        for subdir in ("cv", "audio", "reports"):
            folder = f"{STORAGE_DIR}/{subdir}/{candidate_id}"
            try:
                shutil.rmtree(folder, ignore_errors=True)
            except OSError:
                logger.exception("Failed to remove storage folder %s during hard delete", folder)

    return {"status": "deleted", "job_id": job_id, "candidates_deleted": len(candidate_ids)}


@router.get("/{job_id}/reports", response_model=list[JobReportListItemOut])
def list_job_reports(job_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """Every GENUINELY invited candidate for this job with their interview/decision pipeline stage
    — powers the Laporan page (#15 + Round 12/13/14 follow-up). Round 13: candidates who haven't
    even been invited yet are excluded entirely (not just coarsely labeled "Menunggu Wawancara") —
    Laporan is about tracking invited candidates through interview -> decision, not surfacing the
    whole uninvited CV pool, which is the Kandidat page's job.

    Round 14 follow-up (real bug, user-reported): `invited_at`/`contact_email` are NOT proof of a
    real invite — `invited_at` is set the moment HR opens the invite modal (token generation), and
    `contact_email` can be added/edited long after with no send action ever happening. The only
    real signal that an invite email was actually dispatched is `invite_email_sent_at`
    (routers/candidates.py::send_candidate_invite_email) — filtering on that instead mirrors the
    identical fix in routers/matching.py and CandidateDetailPage.tsx/ShortlistPage.tsx's status
    logic."""
    _get_scoped_job(db, job_id, hr["company_id"])

    candidates = [c for c in repo.candidates.list(db, job_id=job_id) if c.invite_email_sent_at is not None]
    items = []
    for candidate in candidates:
        interview_completed = len(repo.interview_answers.list(db, candidate_id=candidate.id)) > 0
        gap_rows = repo.skill_gap_results.list(db, candidate_id=candidate.id, job_id=job_id)
        processing_complete = interview_completed and bool(gap_rows) and gap_rows[0].upskilling_plan is not None
        decisions = repo.hr_decisions.list(db, candidate_id=candidate.id)
        decision = decisions[0] if decisions else None
        scores = repo.match_scores.list(db, candidate_id=candidate.id, job_id=job_id)
        items.append(
            JobReportListItemOut(
                candidate_id=candidate.id,
                alias=candidate.alias,
                interview_completed=interview_completed,
                processing_complete=processing_complete,
                decision=decision.decision if decision else None,
                decided_at=decision.decided_at.isoformat() if decision else None,
                match_score=scores[0].overall_score if scores else None,
                report_sent=decision.report_sent_at is not None if decision else False,
            )
        )
    return items


@router.get("/{job_id}/competencies", response_model=list[CompetencyOut])
def get_job_competencies(
    job_id: int,
    include_dismissed: bool = False,
    hr=Depends(get_current_hr),
    db: Session = Depends(get_db),
):
    """Defaults to active-only (what's actually required). include_dismissed=true returns the
    full list including the "recommended pool" — used by CompetencyEditor's restore section."""
    _get_scoped_job(db, job_id, hr["company_id"])
    if include_dismissed:
        return repo.jd_competencies.list(db, job_id=job_id)
    return repo.jd_competencies.list(db, job_id=job_id, status="active")


def _get_scoped_competency(db: Session, job_id: int, competency_id: int, company_id: int):
    _get_scoped_job(db, job_id, company_id)
    competency = repo.jd_competencies.get(db, competency_id)
    if not competency or competency.job_id != job_id:
        raise HTTPException(status_code=404, detail="Competency not found")
    return competency


def _require_no_scored_candidates(db: Session, job_id: int) -> None:
    """Round-3 follow-up #9 (2026-07-19): backend-level enforcement (not just a UI-level lockout,
    see JobDetailPage.tsx removing its edit entry point entirely) that a job's required-competency
    list can't be changed once at least one candidate has already been scored against it — the
    real invariant this protects is "skill-gap analysis for a candidate should never silently go
    stale relative to a competency list that changed after the fact." A job with zero scored
    candidates yet (including one someone navigated back to right after creation) can still be
    freely edited — the constraint is about protecting EXISTING analyses, not about locking based
    on time-since-creation."""
    if repo.match_scores.list(db, job_id=job_id):
        raise HTTPException(
            status_code=400,
            detail="Kompetensi wajib tidak dapat diubah setelah ada kandidat yang dinilai untuk lowongan ini.",
        )


def _active_duplicate_exists(db: Session, job_id: int, name: str, exclude_id: int | None = None) -> bool:
    """Same duplicate-prevention rule as _extract_and_store_competencies, applied to restore/add
    too — both can otherwise create a second ACTIVE row with a name that's already active
    (restore: a re-extraction beat it to the name while it sat dismissed; add: HR types a name
    that's already there)."""
    name_key = name.strip().lower()
    for row in repo.jd_competencies.list(db, job_id=job_id, status="active"):
        if row.id != exclude_id and row.competency_name.strip().lower() == name_key:
            return True
    return False


@router.post("/{job_id}/competencies/{competency_id}/dismiss", response_model=CompetencyOut)
def dismiss_competency(
    job_id: int, competency_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """Never deletes the row — flips it to 'dismissed' so it stops counting as required
    everywhere (matching, report, candidate detail all filter to status='active') while staying
    visible/restorable as a recommendation (#4/#7)."""
    competency = _get_scoped_competency(db, job_id, competency_id, hr["company_id"])
    _require_no_scored_candidates(db, job_id)
    competency.status = "dismissed"
    db.commit()
    db.refresh(competency)
    return competency


@router.post("/{job_id}/competencies/{competency_id}/restore", response_model=CompetencyOut)
def restore_competency(
    job_id: int, competency_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    competency = _get_scoped_competency(db, job_id, competency_id, hr["company_id"])
    _require_no_scored_candidates(db, job_id)
    if _active_duplicate_exists(db, job_id, competency.competency_name, exclude_id=competency.id):
        raise HTTPException(
            status_code=400,
            detail="A competency with this name is already active — it may have been re-extracted while dismissed",
        )
    competency.status = "active"
    db.commit()
    db.refresh(competency)
    return competency


@router.post("/{job_id}/competencies", response_model=CompetencyOut)
def add_competency(
    job_id: int, body: CompetencyAddRequest, hr=Depends(get_current_hr), db: Session = Depends(get_db)
):
    """HR adds a custom competency the AI extraction missed — created directly as active."""
    _get_scoped_job(db, job_id, hr["company_id"])
    _require_no_scored_candidates(db, job_id)
    if _active_duplicate_exists(db, job_id, body.competency_name):
        raise HTTPException(status_code=400, detail="A competency with this name is already active")
    return repo.jd_competencies.create(
        db,
        job_id=job_id,
        competency_name=body.competency_name,
        importance_level=body.importance_level,
        status="active",
        source="custom",
    )
