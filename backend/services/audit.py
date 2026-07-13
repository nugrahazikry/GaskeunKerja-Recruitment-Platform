from sqlalchemy.orm import Session

from db import repositories as repo


def log(db: Session, actor: str, action: str, entity_type: str, entity_id: int, **metadata) -> None:
    """Write an audit_log row. actor: an hr_user_id (int-as-str), "system", or "candidate"."""
    repo.audit_log.create(
        db,
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        audit_metadata=metadata or None,
    )
