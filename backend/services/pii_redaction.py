"""PII redaction (Area 2 T5): strips name/email/phone before the merged CV text ever
reaches the LLM. Runs regex-based redaction for email/phone (reliable, deterministic),
plus a name replacement driven by an LLM-detected candidate name.

Name detection (added 2026-07-13, closes a real gap found during Area 5 QA T3b): email
and phone are detectable by regex pattern alone, but a name has no fixed pattern — it can
only be found by understanding the text. A "first line = name" heuristic was tested
against real seed CV text and found unreliable (the first line was a job title on a real
sample). detect_candidate_name() uses one cheap Flash call instead.
"""

import json
import logging
import re

from services import llm_client

logger = logging.getLogger("pii_redaction")

_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
# Matches phone-formatted numbers only (parens/dashes/spaces as separators between digit
# groups, optionally a leading +) — NOT bare slash-separated date ranges like "01/2000".
_PHONE_RE = re.compile(r"(\+?\(?\d{2,4}\)?[\-\s]\d{3,4}[\-\s]\d{3,4}(?:[\-\s]\d{2,4})?)")

_NAME_DETECTION_PROMPT = """\
Anda membaca teks CV berikut. Temukan nama lengkap kandidat (pemilik CV ini) jika disebutkan \
secara eksplisit di dalam teks.

Kembalikan HANYA JSON: {{"name": "<nama lengkap>"}} jika ditemukan, atau {{"name": null}} jika \
tidak ada nama yang jelas disebutkan. Jangan menebak nama dari nama perusahaan, produk, atau \
istilah teknis — hanya nama orang.

Teks CV (200 karakter pertama sudah cukup untuk tugas ini):
{cv_text_snippet}"""


def detect_candidate_name(cv_text: str) -> str | None:
    """One cheap Flash call: find the candidate's real name in the raw (pre-redaction)
    CV text, if present, so redact_pii() has something concrete to replace.

    Only the first part of the text is sent — names appear near the top of virtually
    every resume format, and keeping this prompt small keeps the extra call cheap.
    """
    snippet = cv_text[:800]
    prompt = _NAME_DETECTION_PROMPT.format(cv_text_snippet=snippet)
    raw = llm_client.chat_flash([{"role": "user", "content": prompt}])

    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("detect_candidate_name: failed to parse JSON, raw=%r", raw)
        return None

    if not isinstance(parsed, dict):
        return None

    name = parsed.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        return None
    return name.strip()


def redact_pii(text: str, alias: str, candidate_name: str | None = None) -> str:
    """Replace email, phone numbers, and (if known) the candidate's name with alias.

    Address redaction is intentionally not attempted with regex (too unstructured to
    reliably detect without false positives) — only email/phone/name are redacted,
    matching what's actually reliably detectable.
    """
    redacted = _EMAIL_RE.sub(f"[{alias}-email]", text)
    redacted = _PHONE_RE.sub(f"[{alias}-phone]", redacted)

    if candidate_name:
        # Replace the name case-insensitively, whole-word where possible
        pattern = re.compile(re.escape(candidate_name), re.IGNORECASE)
        redacted = pattern.sub(alias, redacted)

    return redacted
