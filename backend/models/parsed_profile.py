from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class ParsedProfile(Base):
    __tablename__ = "parsed_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    skills: Mapped[dict] = mapped_column(JSONB, nullable=False)
    experience: Mapped[dict] = mapped_column(JSONB, nullable=False)
    qualifications: Mapped[dict] = mapped_column(JSONB, nullable=False)
    raw_cv_path: Mapped[str] = mapped_column(String, nullable=False)
    parsed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
