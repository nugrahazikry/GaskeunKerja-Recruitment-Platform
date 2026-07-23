from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class SkillGapResult(Base):
    """Persisted skill-gap analysis for one candidate x job pair (Round-2 polish, 2026-07-17).

    Computed once (alongside the match score) instead of live on every candidate-detail /
    report view — analyze_skill_gap() runs 3 self-consistency LLM votes and was measured to
    take ~25-30s per call, repeated identically on every single page load with zero caching.
    """

    __tablename__ = "skill_gap_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    gap_summary: Mapped[str] = mapped_column(String, nullable=False)
    missing_competencies: Mapped[list] = mapped_column(JSONB, nullable=False)
    matched_competencies: Mapped[list] = mapped_column(JSONB, nullable=False)
    development_priority: Mapped[str | None] = mapped_column(String, nullable=True)
    # Round-3 follow-up (2026-07-19): {competency_name: 1-3} for each entry in matched_competencies
    # — how strongly the candidate's actual experience text evidences that competency. Drives the
    # new proficiency-weighted ranking score in services/matching.py (replacing semantic+graph
    # scoring) so candidates who match the same competency set can still be ranked apart by depth.
    competency_proficiency: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # Round-3 follow-up #4 (2026-07-19): candidate-detail/laporan redesign, "Key Strengths" +
    # "Resume Action Items (ATS)" sections from the Tahap 2 template — computed ONCE here
    # (alongside the rest of skill-gap analysis) via one extra LLM call, not live per page view.
    key_strengths: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    resume_action_items: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    # Round 7 (2026-07-21, user decision): interview-performance-based counterparts to
    # key_strengths/resume_action_items above — same {"title", "description"} shape. Deliberately
    # NOT computed alongside the CV-based fields at match time (this row is created before any
    # interview happens); see services/skillgap.py::update_recommendation_extras_after_interview(),
    # called once the candidate's interview is fully transcribed+scored (from
    # services/interview_answers.py::process_answer). Nullable — empty until that point.
    interview_key_strengths: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    interview_feedback: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    # Round 8 (2026-07-21, user decision): fully LLM-generated upskilling plan
    # ({competency_name: {"low_effort": [...], "medium_effort": [...], "high_effort": [...]}}),
    # replacing the old deterministic competency_framework/resource_library lookup (which only
    # ever covered ~10 hand-curated competencies for one demo role). Computed alongside
    # interview_key_strengths/interview_feedback in update_recommendation_extras_after_interview()
    # — see services/skillgap.py::generate_upskilling_plan(). Nullable — empty until then.
    upskilling_plan: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
