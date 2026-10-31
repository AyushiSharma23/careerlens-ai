"""Small helpers for cleaning text before analysis."""

import re


def normalize_text(text: str) -> str:
    """Lowercase the text and replace any run of whitespace with one space."""
    text = text.replace("\u00a0", " ")  # non-breaking space (common in PDFs)
    text = text.lower()
    text = re.sub(r"\s+", " ", text)  # spaces, tabs and newlines -> one space
    return text.strip()