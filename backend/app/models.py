"""Database tables."""

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Analysis(Base):
    """One saved resume-to-job analysis. The resume itself is NOT stored."""

    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_title: Mapped[str] = mapped_column(String(200))
    company: Mapped[str] = mapped_column(String(200), default="")
    job_description: Mapped[str] = mapped_column(Text)
    score: Mapped[float] = mapped_column(Float)
    skill_coverage: Mapped[float] = mapped_column(Float)
    text_similarity: Mapped[float] = mapped_column(Float)
    matched_skills: Mapped[list] = mapped_column(JSON)
    missing_skills: Mapped[list] = mapped_column(JSON)
    explanation: Mapped[list] = mapped_column(JSON)
    suggestions: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)