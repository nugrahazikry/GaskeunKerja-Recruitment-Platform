from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import repositories as repo
from db.session import get_db
from routers.auth import get_current_hr
from services.delivery import NoEmailAddressError, NoTelegramLinkError, send_report
from services.report import build_interview_answers, build_report
from services.report_pdf import render_report_pdf

router = APIRouter(prefix="/candidates", tags=["report"])


class UpskillingItemOut(BaseModel):
    title: str
    description: str


class UpskillingPlanOut(BaseModel):
    low_effort: list[UpskillingItemOut]
    medium_effort: list[UpskillingItemOut]
    high_effort: list[UpskillingItemOut]


class UpskillingSectionOut(BaseModel):
    # Defaulted (not required): upskilling_plan is computed by an LLM call AFTER the interview
    # finishes (services/skillgap.py::update_recommendation_extras_after_interview) and can still
    # be {} if that call hasn't run yet or timed out — a real bug found 2026-07-22 (candidate 36's
    # upskilling LLM call timed out mid-pipeline) hard-500'd this whole endpoint over it, when an
    # empty section is a legitimate, displayable state.
    kompetensi_belum_terpenuhi: dict[str, UpskillingPlanOut] = {}
    area_pengembangan_wawancara: dict[str, UpskillingPlanOut] = {}


class KeyStrengthOut(BaseModel):
    title: str
    description: str


class ResumeActionItemOut(BaseModel):
    original: str
    improved: str


class RubricScoreOut(BaseModel):
    criterion_name: str
    score: int
    rationale: str


class InterviewAnswerOut(BaseModel):
    question_text: str
    summary_text: str | None
    transcript_text: str | None
    video_url: str
    rubric_scores: list[RubricScoreOut]


class ReportOut(BaseModel):
    candidate_alias: str
    job_title: str
    # 2026-07-22 (user-requested): lets ReportPage.tsx show "Ambil Keputusan" only pre-decision,
    # and the actual outcome once one exists — None means no hr_decisions row yet.
    decision: str | None
    gap_summary: str
    development_priority: str | None
    matched_competencies: list[str]
    missing_competencies: list[str]
    key_strengths: list[KeyStrengthOut]
    resume_action_items: list[ResumeActionItemOut]
    interview_key_strengths: list[KeyStrengthOut]
    interview_feedback: list[KeyStrengthOut]
    upskilling_plan: UpskillingSectionOut
    interview_overall_score: float | None
    interview_answers: list[InterviewAnswerOut]
    cv_summary: str | None
    skills: list[str]
    skills_implicit: list
    experience: list
    qualifications: list
    education_level: str | None
    major: str | None
    education_history: list
    certifications: list
    featured_projects: list
    organization_experience: list


def _get_scoped_candidate(db: Session, candidate_id: int, company_id: int):
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    job = repo.jobs.get(db, candidate.job_id)
    if not job or job.company_id != company_id:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


def _require_decision(db: Session, candidate_id: int):
    decisions = repo.hr_decisions.list(db, candidate_id=candidate_id)
    if not decisions:
        raise HTTPException(
            status_code=400, detail="Cannot generate report: no HR decision recorded yet"
        )


def _require_report_ready(db: Session, candidate_id: int, job_id: int):
    """Viewing a report only needs the interview content to exist (Round 12 follow-up) — a
    candidate in "Menunggu Keputusan HR" has real interview answers/rubric scores/skill-gap
    analysis to show, just no decision yet. Actually SENDING a report to the candidate still
    requires a decision (_require_decision, unchanged, used by send_candidate_report below) —
    emailing an undecided report to someone makes no sense even if viewing one internally does.

    2026-07-22 (user-reported real bug/"glitch"): interview answers existing is NOT the same as
    the post-interview LLM chain having finished — a candidate could be viewed mid-pipeline with
    upskilling_plan still null/empty, rendering an apparently-final report that's actually
    incomplete. Now also requires skill_gap_results.upskilling_plan to be populated (the last
    field update_recommendation_extras_after_interview() writes, success or graceful fallback) —
    matches the same gate now applied to JobReportListItemOut.processing_complete
    (routers/jobs.py::list_job_reports)."""
    if not repo.interview_answers.list(db, candidate_id=candidate_id):
        raise HTTPException(
            status_code=400, detail="Cannot generate report: interview not completed yet"
        )
    gap_rows = repo.skill_gap_results.list(db, candidate_id=candidate_id, job_id=job_id)
    if not gap_rows or gap_rows[0].upskilling_plan is None:
        raise HTTPException(
            status_code=400,
            detail="Laporan belum selesai diproses oleh sistem (analisis AI masih berjalan) — silakan coba lagi dalam beberapa menit",
        )


def _build_interview_answers(db: Session, candidate_id: int) -> list[InterviewAnswerOut]:
    """HR-only "Wawancara" section on the laporan PAGE — adds a playable video_url on top of
    services.report.build_interview_answers()'s plain-dict data (the PDF renderer uses that same
    function directly, without video_url, since a static PDF can't embed one)."""
    return [
        InterviewAnswerOut(
            question_text=a["question_text"],
            summary_text=a["summary_text"],
            transcript_text=a["transcript_text"],
            video_url=f"/candidates/{candidate_id}/answers/{a['answer_id']}/audio",
            rubric_scores=[RubricScoreOut(**r) for r in a["rubric_scores"]],
        )
        for a in build_interview_answers(db, candidate_id)
    ]


@router.get("/{candidate_id}/report", response_model=ReportOut)
def get_candidate_report(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    candidate = _get_scoped_candidate(db, candidate_id, hr["company_id"])
    _require_report_ready(db, candidate_id, candidate.job_id)
    report = build_report(db, candidate_id, candidate.job_id)
    decisions = repo.hr_decisions.list(db, candidate_id=candidate_id)
    return ReportOut(
        **report,
        decision=decisions[0].decision if decisions else None,
        interview_answers=_build_interview_answers(db, candidate_id),
    )


@router.get("/{candidate_id}/report/pdf")
def get_candidate_report_pdf(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """HR-facing PDF preview ("Lihat Laporan") — direct mirror of candidate_detail.py's
    get_candidate_cv: generates the same PDF build_report()/render_report_pdf() would email, but
    renders it fresh in-memory for viewing instead of writing it to storage/reports/ (that write
    only happens as a side effect of actually sending, in services.delivery.send_report)."""
    candidate = _get_scoped_candidate(db, candidate_id, hr["company_id"])
    _require_report_ready(db, candidate_id, candidate.job_id)
    report = build_report(db, candidate_id, candidate.job_id)
    interview_answers = build_interview_answers(db, candidate_id)
    pdf_bytes = render_report_pdf(report, interview_answers)
    return Response(content=pdf_bytes, media_type="application/pdf")


@router.post("/{candidate_id}/send-report")
def send_candidate_report(candidate_id: int, hr=Depends(get_current_hr), db: Session = Depends(get_db)):
    """HR triggers delivery with one click — PDF + summary auto-sent via Telegram."""
    _get_scoped_candidate(db, candidate_id, hr["company_id"])
    _require_decision(db, candidate_id)

    try:
        result = send_report(db, candidate_id)
    except NoTelegramLinkError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except NoEmailAddressError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return {"status": "sent", **result}
