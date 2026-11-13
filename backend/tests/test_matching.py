from app.matching import analyze_match, calculate_skill_coverage, calculate_text_similarity


def test_skill_coverage_counts_only_job_skills():
    matched, missing, coverage = calculate_skill_coverage(
        resume_skills=["Python", "Git", "GitHub"],
        job_skills=["Python", "Docker"],
    )
    assert matched == ["Python"]
    assert missing == ["Docker"]
    assert coverage == 0.5


def test_skill_coverage_with_no_job_skills_is_zero():
    matched, missing, coverage = calculate_skill_coverage(["Python"], [])
    assert (matched, missing, coverage) == ([], [], 0.0)


def test_identical_texts_have_similarity_close_to_one():
    text = "python developer with sql experience"
    assert calculate_text_similarity(text, text) > 0.99


def test_similarity_of_empty_text_is_zero():
    assert calculate_text_similarity("", "python developer") == 0.0


def test_score_follows_the_documented_formula():
    resume = "Built a small web app using Python, SQL and React. Used Git and GitHub."
    job = "We need an intern with Python, SQL, React and Docker. Experience with AWS, REST APIs and Git is a plus."
    result = analyze_match(resume, job)
    expected = round(0.7 * result["skill_coverage"] + 0.3 * result["text_similarity"], 1)
    assert abs(result["score"] - expected) <= 0.1
    assert result["matched_skills"] == ["Python", "React", "SQL", "Git"]
    assert result["missing_skills"] == ["Docker", "AWS", "REST API"]


def test_job_without_known_skills_uses_text_similarity_only():
    result = analyze_match("I enjoy cricket and reading.", "We are hiring a chef for our kitchen.")
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["score"] == result["text_similarity"]