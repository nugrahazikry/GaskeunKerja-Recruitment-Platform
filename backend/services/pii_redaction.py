"""PII redaction (Area 2 T5): strips name/email/phone before the merged CV text ever
reaches the LLM. Runs regex-based redaction for email/phone (reliable, deterministic),
plus a name replacement driven by the candidate's own extracted-name guess.
"""

import re

_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
# Matches phone-formatted numbers only (parens/dashes/spaces as separators between digit
# groups, optionally a leading +) — NOT bare slash-separated date ranges like "01/2000".
_PHONE_RE = re.compile(r"(\+?\(?\d{2,4}\)?[\-\s]\d{3,4}[\-\s]\d{3,4}(?:[\-\s]\d{2,4})?)")


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
