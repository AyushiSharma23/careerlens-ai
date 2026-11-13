"""Compare a resume with a job description and produce an explainable score."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.skills import detect_skills
from app.text_utils import normalize_text

# Final score = SKILL_WEIGHT * skill coverage + TEXT_WEIGHT * text similarity
SKILL_WEIGHT = 0.7
TEXT_WEIGHT = 0.3


def calculate_text_similarity(resume_text: str, job_text: str) -> float:
    """Return TF-IDF cosine similarity between two texts (0.0 to 1.0)."""
    resume_clean = normalize_text(resume_text)
    job_clean = normalize_text(job_text)
    if not resume_clean or not job_clean:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_clean, job_clean])
    except ValueError:
        # Happens when a text has no usable words (for example only stop words).
        return 0.0

    return float(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0])


def calculate_skill_coverage(resume_skills: list[str], job_skills: list[str]):
    """Return (matched, missing, coverage) for the skills the job asks for."""
    resume_skill_set = set(resume_skills)
    matched = [skill for skill in job_skills if skill in resume_skill_set]
    missing = [skill for skill in job_skills if skill not in resume_skill_set]
    coverage = len(matched) / len(job_skills) if job_skills else 0.0
    return matched, missing, coverage


def build_explanation(job_skills, matched, coverage, similarity, score) -> list[str]:
    """Write the score calculation in plain sentences."""
    lines = []
    if job_skills:
        lines.append(
            f"The job description mentions {len(job_skills)} skills from our dictionary. "
            f"Your resume covers {len(matched)} of them ({coverage * 100:.1f}%)."
        )
        lines.append(f"Text similarity (TF-IDF with cosine similarity) is {similarity * 100:.1f}%.")
        lines.append(
            f"Final score = {SKILL_WEIGHT * 100:.0f}% x skill coverage + "
            f"{TEXT_WEIGHT * 100:.0f}% x text similarity = {score * 100:.1f}%."
        )
    else:
        lines.append("No skills from our dictionary were found in the job description.")
        lines.append(
            f"The score therefore uses text similarity only: {similarity * 100:.1f}%."
        )
    return lines


def build_suggestions(missing_skills: list[str]) -> list[str]:
    """Turn each missing skill into one practical suggestion."""
    return [
        f"{skill} appears in the job description but not in your resume. "
        f"If you have used it, add it to your skills section or a project. "
        f"If not, consider learning it."
        for skill in missing_skills
    ]


def analyze_match(resume_text: str, job_text: str) -> dict:
    """Compare a resume with a job description and return an explainable result."""
    resume_skills = detect_skills(resume_text)
    job_skills = detect_skills(job_text)

    matched, missing, coverage = calculate_skill_coverage(resume_skills, job_skills)
    similarity = calculate_text_similarity(resume_text, job_text)

    if job_skills:
        score = SKILL_WEIGHT * coverage + TEXT_WEIGHT * similarity
    else:
        score = similarity

    return {
        "score": round(score * 100, 1),
        "skill_coverage": round(coverage * 100, 1),
        "text_similarity": round(similarity * 100, 1),
        "matched_skills": matched,
        "missing_skills": missing,
        "explanation": build_explanation(job_skills, matched, coverage, similarity, score),
        "suggestions": build_suggestions(missing),
    }


if __name__ == "__main__":
    sample_resume = (
        "Built a small web app using Python, SQL and React. "
        "Used Git and GitHub for version control."
    )
    sample_job = (
        "We need a software intern with Python, SQL, React and Docker. "
        "Experience with AWS, REST APIs and Git is a plus."
    )

    result = analyze_match(sample_resume, sample_job)
    print(f"Estimated match score: {result['score']}%")
    print("Matched skills:", result["matched_skills"])
    print("Missing skills:", result["missing_skills"])
    print("How the score was calculated:")
    for line in result["explanation"]:
        print(" -", line)
    print("Suggestions:")
    for line in result["suggestions"]:
        print(" -", line)