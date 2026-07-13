from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from db.session import Base


class CompetencyFramework(Base):
    __tablename__ = "competency_framework"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_role: Mapped[str] = mapped_column(String, nullable=False)
    competency_name: Mapped[str] = mapped_column(String, nullable=False)
    level_description: Mapped[str] = mapped_column(Text, nullable=False)
    related_competency_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False, default=list)


class ResourceLibrary(Base):
    __tablename__ = "resource_library"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competency_id: Mapped[int] = mapped_column(ForeignKey("competency_framework.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    duration: Mapped[str] = mapped_column(String, nullable=False)
    milestone_description: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(String, nullable=True)
