import os
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from config import STORAGE_DIR
from db import repositories as repo
from services import telegram_client
from services.report import build_report
from services.report_pdf import render_report_pdf


class NoTelegramLinkError(Exception):
    """Raised when the candidate hasn't linked their Telegram chat yet."""


def send_report(db: Session, candidate_id: int) -> dict:
    """Generates the PDF, saves it, and delivers it + a summary via Telegram.

    Requires an hr_decisions row (checked by build_report's caller) and a linked
    telegram_chat_id — raises NoTelegramLinkError if the candidate hasn't linked yet.
    """
    candidate = repo.candidates.get(db, candidate_id)
    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found")
    if not candidate.telegram_chat_id:
        raise NoTelegramLinkError(f"Candidate {candidate_id} has not linked Telegram yet")

    report = build_report(db, candidate_id, candidate.job_id)
    pdf_bytes = render_report_pdf(report)

    pdf_path = f"{STORAGE_DIR}/reports/{candidate_id}/laporan.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    chat_id = int(candidate.telegram_chat_id)
    telegram_client.send_document(
        chat_id, pdf_path, caption=f"Laporan pengembangan untuk {candidate.alias}"
    )
    telegram_client.send_message(chat_id, report["gap_summary"])

    decisions = repo.hr_decisions.list(db, candidate_id=candidate_id)
    if decisions:
        decisions[0].report_sent_at = datetime.now(timezone.utc)
        db.commit()

    return {"pdf_path": pdf_path, "chat_id": chat_id}
