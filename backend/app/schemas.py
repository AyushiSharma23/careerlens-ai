"""Shapes of the data the API sends back."""

from pydantic import BaseModel


class AnalysisResult(BaseModel):
    score: float
    skill_coverage: float
    text_similarity: float
    matched_skills: list[str]
    missing_skills: list[str]
    explanation: list[str]
    suggestions: list[str]