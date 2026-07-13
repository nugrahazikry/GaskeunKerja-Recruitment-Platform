"""Audio retention policy (Area 3 T9, supports UU PDP).

Scope: applies ONLY to real, consented recordings — i.e. the 1 live demo candidate's audio.
The 2-3 synthetic candidates' pre-made .webm clips are seed fixtures, not personal data
collected under consent (they have no consent_records row — see services/consent.py),
so cleanup_expired_audio() below never touches them: it only iterates candidates that
actually have a consent record.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy.orm import Session

from db import repositories as repo

RETENTION_DAYS = 30


def is_audio_expired(consented_at: datetime, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    return now - consented_at > timedelta(days=RETENTION_DAYS)


def cleanup_expired_audio(db: Session, storage_root: str, now: datetime | None = None) -> list[int]:
    """Manually callable cleanup: deletes audio files for candidates whose consent record
    is older than RETENTION_DAYS. Returns the list of candidate_ids cleaned up.

    Only ever considers candidates with a real consent_records row — seed/synthetic
    candidates (no consent row) are structurally excluded, not filtered out by a flag.
    """
    cleaned: list[int] = []
    all_consents = repo.consent_records.list(db, consent_given=True)

    for record in all_consents:
        if not is_audio_expired(record.consented_at, now=now):
            continue

        candidate_audio_dir = Path(storage_root) / "audio" / str(record.candidate_id)
        if candidate_audio_dir.exists():
            for file in candidate_audio_dir.rglob("*.webm"):
                file.unlink()
        cleaned.append(record.candidate_id)

    return cleaned
