import logging

import httpx

from config import TELEGRAM_BOT_TOKEN

logger = logging.getLogger("telegram_client")

_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def get_me() -> dict:
    r = httpx.get(f"{_BASE_URL}/getMe")
    r.raise_for_status()
    return r.json()["result"]


def get_updates(offset: int | None = None) -> list[dict]:
    """Poll for incoming messages (e.g. /start <token> from the deep-link)."""
    params = {"timeout": 0}
    if offset is not None:
        params["offset"] = offset
    r = httpx.get(f"{_BASE_URL}/getUpdates", params=params)
    r.raise_for_status()
    return r.json()["result"]


def extract_start_token(update: dict) -> tuple[int, str] | None:
    """From a getUpdates entry, extract (chat_id, token) if it's a /start <token> deep-link message."""
    message = update.get("message")
    if not message:
        return None
    text = message.get("text", "")
    if not text.startswith("/start "):
        return None
    chat_id = message["chat"]["id"]
    token = text.removeprefix("/start ").strip()
    return chat_id, token


def send_message(chat_id: int, text: str) -> dict:
    r = httpx.post(f"{_BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})
    r.raise_for_status()
    logger.info("sendMessage chat_id=%s len=%d", chat_id, len(text))
    return r.json()["result"]


def send_document(chat_id: int, file_path: str, caption: str | None = None) -> dict:
    with open(file_path, "rb") as f:
        files = {"document": f}
        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
        r = httpx.post(f"{_BASE_URL}/sendDocument", data=data, files=files)
    r.raise_for_status()
    logger.info("sendDocument chat_id=%s file=%s", chat_id, file_path)
    return r.json()["result"]
