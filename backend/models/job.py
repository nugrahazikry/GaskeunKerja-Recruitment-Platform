from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    responsibilities: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[str] = mapped_column(Text, nullable=False)
    qualifications: Mapped[str] = mapped_column(Text, nullable=False)
    # Round-3 Task 20: extracted from the Kualifikasi text alongside competencies. Nullable — a
    # JD that doesn't state an education requirement leaves these empty (no eligibility gate).
    required_education_level: Mapped[str | None] = mapped_column(String, nullable=True)
    required_major: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class JDCompetency(Base):
    __tablename__ = "jd_competencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    competency_name: Mapped[str] = mapped_column(String, nullable=False)
    importance_level: Mapped[float] = mapped_column(nullable=False, default=1.0)
    # "active" (default) | "dismissed" — dismissing a competency never deletes the row, it just
    # flips this so it stops counting as required everywhere while staying restorable (Round-2
    # polish, 2026-07-17: the "recommended pool" behavior requested for #4/#7).
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    # "ai" (default, from extraction) | "custom" (HR-added via the "+ Tambah kompetensi" input) —
    # the recommended-pool UI only ever resurfaces dismissed "ai" rows; a dismissed custom one was
    # a mistake the HR typed in themselves, not something AI suggested, so it shouldn't come back
    # as a "recommendation."
    source: Mapped[str] = mapped_column(String, nullable=False, default="ai")
