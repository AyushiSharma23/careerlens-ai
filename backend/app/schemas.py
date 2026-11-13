"""Shapes of the data the API receives and sends back."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class AnalysisResult(BaseModel):
    score: float
    skill_coverage: float
    text_similarity: float
    matched_skills: list[str]
    missing_skills: list[str]
    explanation: list[str]
    suggestions: list[str]


class AnalysisRecord(AnalysisResult):
    """A saved analysis: the result plus its database details."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    job_title: str
    company: str
    created_at: datetime


class ApplicationStatus(str, Enum):
    """The only statuses an application can have."""

    INTERESTED = "Interested"
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"


class ApplicationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    job_title: str = Field(min_length=1, max_length=200)
    company: str = Field(default="", max_length=200)
    status: ApplicationStatus = ApplicationStatus.INTERESTED
    notes: str = ""
    analysis_id: int | None = None


class ApplicationUpdate(BaseModel):
    """Every field is optional: only the fields that are sent get changed."""

    model_config = ConfigDict(str_strip_whitespace=True)

    job_title: str | None = Field(default=None, min_length=1, max_length=200)
    company: str | None = Field(default=None, max_length=200)
    status: ApplicationStatus | None = None
    notes: str | None = None


class ApplicationRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    analysis_id: int | None
    job_title: str
    company: str
    status: ApplicationStatus
    notes: str
    created_at: datetime
    updated_at: datetime


class ApplicationStats(BaseModel):
    total: int
    by_status: dict[str, int]