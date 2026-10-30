"""Detect technical skills mentioned in a piece of text."""

import re

# Each skill maps to the aliases (spellings) people use for it.
# Aliases are written in lowercase because we lowercase the text before searching.
SKILL_ALIASES = {
    "Python": ["python"],
    "C++": ["c++", "cpp"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "React": ["react", "reactjs", "react.js"],
    "SQL": ["sql"],
    "MySQL": ["mysql"],
    "Git": ["git"],
    "FastAPI": ["fastapi"],
    "Docker": ["docker"],
}


def detect_skills(text: str) -> list[str]:
    """Return the skills from SKILL_ALIASES that appear in `text`."""
    lowered_text = text.lower()
    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            # Match the alias only as a whole word:
            # not preceded or followed by a letter or digit.
            pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
            if re.search(pattern, lowered_text):
                found_skills.append(skill)
                break  # one matching alias is enough for this skill

    return found_skills


if __name__ == "__main__":
    sample_resume = (
        "I built a small project using Python and MySQL. "
        "I know C++ and JavaScript, and I use GitHub for my code. "
        "I am learning React.js."
        "I am familiar with docker."
    )
    print(detect_skills(sample_resume))