from sqlalchemy.orm import Session

from db import repositories as repo


class ConsentRequiredError(Exception):
    """Raised when interview processing is attempted for a candidate with no consent record."""


def has_consent(db: Session, candidate_id: int) -> bool:
    records = repo.consent_records.list(db, candidate_id=candidate_id, consent_given=True)
    return len(records) > 0


def require_consent(db: Session, candidate_id: int) -> None:
    """Hard gate: raise if this candidate has no consent_records row with consent_given=True.

    Enforced before any interview-answer intake (Area 2 T10) — a 403 at the API layer.
    """
    if not has_consent(db, candidate_id):
        raise ConsentRequiredError(f"No consent record for candidate {candidate_id}")


def record_consent(db: Session, candidate_id: int, consent_text_version: str):
    return repo.consent_records.create(
        db,
        candidate_id=candidate_id,
        consent_given=True,
        consent_text_version=consent_text_version,
    )
