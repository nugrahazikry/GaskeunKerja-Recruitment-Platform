from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class ParsedProfile(Base):
    __tablename__ = "parsed_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    skills: Mapped[dict] = mapped_column(JSONB, nullable=False)
    experience: Mapped[dict] = mapped_column(JSONB, nullable=False)
    qualifications: Mapped[dict] = mapped_column(JSONB, nullable=False)
    raw_cv_path: Mapped[str] = mapped_column(String, nullable=False)
    # Round-3 Task 20: extracted alongside skills/experience/qualifications. Nullable — a CV
    # that doesn't state education clearly leaves these empty rather than guessing.
    education_level: Mapped[str | None] = mapped_column(String, nullable=True)
    major: Mapped[str | None] = mapped_column(String, nullable=True)
    # Round-3 follow-up #4 (2026-07-19): candidate-detail/laporan redesign to match the Tahap 2
    # "SkillGap AI" template — all extracted in the SAME cv_parser LLM call as skills/experience
    # (one extra JSON field each, not one extra call each). `skills` (existing column) is treated
    # as "explicit skills" for display; skills_implicit is the new soft/inferred-skill list.
    cv_summary: Mapped[str | None] = mapped_column(String, nullable=True)
    skills_implicit: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    education_history: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    certifications: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    featured_projects: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    organization_experience: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    # Round 7 (2026-07-21, user decision, option B): the PDF-extracted, PII-redacted CV text in its
    # ORIGINAL language — captured BEFORE cv_parser's LLM call translates narrative fields to
    # Indonesian (see cv_parser.py's ATURAN BAHASA). Previously this text only ever existed as a
    # local variable in candidate_ingest.py::ingest_cv(), discarded once parsing finished — nothing
    # downstream could recover the candidate's own original wording. Needed so ATS resume-rewrite
    # suggestions (skillgap.py::generate_recommendation_extras) can quote+improve the candidate's
    # ACTUAL CV sentences in their ACTUAL language, instead of the already-Indonesian-translated
    # `experience` field. Nullable — candidates ingested before this column existed have no value.
    raw_text_redacted: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
