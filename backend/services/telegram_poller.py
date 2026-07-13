import asyncio
import logging

from db import repositories as repo
from db.session import SessionLocal
from services import telegram_client

logger = logging.getLogger("telegram_poller")

_POLL_INTERVAL_SECONDS = 3
_last_update_id: int | None = None


def _process_updates(db) -> None:
    global _last_update_id

    offset = _last_update_id + 1 if _last_update_id is not None else None
    updates = telegram_client.get_updates(offset=offset)

    for update in updates:
        _last_update_id = update["update_id"]
        parsed = telegram_client.extract_start_token(update)
        if not parsed:
            continue

        chat_id, token = parsed
        candidates = repo.candidates.list(db, token=token)
        if not candidates:
            logger.warning("Telegram /start with unknown token (ignored)")
            continue

        candidate = candidates[0]
        candidate.telegram_chat_id = str(chat_id)
        db.commit()
        logger.info("Linked Telegram chat_id for candidate_id=%s", candidate.id)


async def run_telegram_poller() -> None:
    """Background loop (started on app startup): polls Telegram's getUpdates for
    /start <token> deep-link messages (Area 1 T8) and writes the resulting chat_id onto
    the matching candidate. Runs inside the FastAPI process — no separate cron/process
    needed for a local MVP with getUpdates (not a webhook)."""
    while True:
        try:
            db = SessionLocal()
            try:
                _process_updates(db)
            finally:
                db.close()
        except Exception:
            logger.exception("Telegram poller iteration failed")
        await asyncio.sleep(_POLL_INTERVAL_SECONDS)
