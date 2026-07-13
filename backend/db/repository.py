from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.session import Base

ModelType = TypeVar("ModelType", bound=Base)


class Repository(Generic[ModelType]):
    """Thin CRUD wrapper over SQLAlchemy — no Alembic, no query-building magic."""

    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> ModelType | None:
        return db.get(self.model, id)

    def list(self, db: Session, **filters) -> list[ModelType]:
        stmt = select(self.model)
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        return list(db.scalars(stmt).all())

    def create(self, db: Session, **fields) -> ModelType:
        obj = self.model(**fields)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
