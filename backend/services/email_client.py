"""Round-3 Task 19: Gmail SMTP client replacing Telegram as the candidate notification channel.
Uses only the Python standard library (smtplib + email) — no new dependency, matching the
project's "local-only, minimal deps" constraint. Mirrors telegram_client.py's shape (thin
functions, no class) for consistency with the existing service style.
"""

import logging
import mimetypes
import smtplib
from email.message import EmailMessage

from config import SMTP_FROM, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USERNAME

logger = logging.getLogger("email_client")


def send_email(to: str, subject: str, body: str, attachment_path: str | None = None) -> None:
    """Sends a plain-text email, optionally with one file attachment. Raises on any SMTP failure
    — callers (delivery.py etc.) are expected to let that propagate as a real error, not swallow
    it silently."""
    message = EmailMessage()
    message["From"] = SMTP_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    if attachment_path:
        content_type, _ = mimetypes.guess_type(attachment_path)
        maintype, subtype = (content_type or "application/octet-stream").split("/", 1)
        with open(attachment_path, "rb") as f:
            message.add_attachment(
                f.read(), maintype=maintype, subtype=subtype, filename=attachment_path.split("/")[-1]
            )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(message)

    logger.info("send_email to=%s subject=%r attachment=%s", to, subject, bool(attachment_path))
