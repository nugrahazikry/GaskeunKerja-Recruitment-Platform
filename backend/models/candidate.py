from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    alias: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    token_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    telegram_chat_id: Mapped[str | None] = mapped_column(String, nullable=True)
    # Round-3 Task 19: auto-extracted from the CV at ingest (before PII redaction), HR-editable.
    # Nullable — a CV without a detectable email leaves this empty until HR fills it in manually.
    contact_email: Mapped[str | None] = mapped_column(String, nullable=True)
    invited_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Round 14 (real bug, user-reported): `invited_at` is set the moment HR opens the invite modal
    # (token generation) — a candidate can sit with a token but no email ever actually sent, or get
    # a contact_email added/edited long after, with no real invite action happening at that point.
    # This is the ONLY real signal that an invite email was actually dispatched
    # (routers/candidates.py::send_candidate_invite_email), and is what "Menunggu Wawancara" status
    # is now gated on everywhere, instead of invited_at/has_email.
    invite_email_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # 2026-07-22 (user-requested): guards services/interview_answers.py::process_answer() from
    # sending the post-interview "terima kasih" email more than once — that function's completion
    # trigger (update_recommendation_extras_after_interview finishing) is "self-electing" among
    # concurrently running per-answer background tasks, which is fine for idempotent DB writes but
    # NOT fine for a one-shot email send, so this timestamp is the check-and-set guard.
    interview_finished_notified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # Internal bookkeeping only, never exposed via any API response — lets
    # seed.process_job_folders detect "this exact file was already ingested" across re-runs without
    # needing the original filename (which may contain the candidate's real name) as a visible alias.
    source_file_path: Mapped[str | None] = mapped_column(String, nullable=True)
