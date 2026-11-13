"""Shapes of the data the API sends back."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


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