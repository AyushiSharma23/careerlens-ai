"""Detect technical skills mentioned in a piece of text."""

import re

from app.text_utils import normalize_text

# Each skill maps to the aliases (spellings) people use for it.
# Aliases are lowercase because the text is lowercased before searching.
SKILL_ALIASES = {
    "Python": ["python"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "csharp"],
    "JavaScript": ["javascript"],
    "TypeScript": ["typescript"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React": ["react", "reactjs", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "Express.js": ["express.js", "expressjs"],
    "Flask": ["flask"],
    "Django": ["django"],
    "FastAPI": ["fastapi"],
    "Bootstrap": ["bootstrap"],
    "Tailwind CSS": ["tailwind css", "tailwindcss", "tailwind"],
    "SQL": ["sql"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb"],
    "SQLite": ["sqlite"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Linux": ["linux"],
    "AWS": ["aws", "amazon web services"],
    "REST API": ["rest api", "rest apis", "restful api", "restful apis", "restful"],
    "CI/CD": ["ci/cd", "cicd"],
    "Data Structures": ["data structures", "dsa"],
    "OOP": ["oop", "oops", "object oriented programming", "object-oriented programming"],
    "DBMS": ["dbms"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "NLP": ["nlp", "natural language processing"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "OpenCV": ["opencv"],
    "Postman": ["postman"],
}


def _build_pattern(aliases: list[str]) -> re.Pattern:
    """Build one regex that matches any alias as a whole word."""
    alternatives = "|".join(re.escape(alias) for alias in aliases)
    # Not preceded or followed by a letter or digit => whole-word match.
    return re.compile(r"(?<![a-z0-9])(?:" + alternatives + r")(?![a-z0-9])")


# Build the regex for every skill once, when the file is first imported.
SKILL_PATTERNS = {skill: _build_pattern(aliases) for skill, aliases in SKILL_ALIASES.items()}


def detect_skills(text: str) -> list[str]:
    """Return the skills from SKILL_ALIASES that appear in `text`."""
    cleaned_text = normalize_text(text)
    return [skill for skill, pattern in SKILL_PATTERNS.items() if pattern.search(cleaned_text)]


if __name__ == "__main__":
    sample_text = (
        "Skills:\nPython,  C++ \n\u2022 React.js\u2022 Node.js\n"
        "JavaScript, GitHub, MySQL. Learning Docker."
    )
    print(detect_skills(sample_text))
