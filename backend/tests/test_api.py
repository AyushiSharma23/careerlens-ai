import pymupdf
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

JOB_TEXT = "We need an intern with Python, SQL, React and Docker."


def make_pdf_bytes(text):
    document = pymupdf.open()
    page = document.new_page()
    if text:
        page.insert_text((72, 72), text)
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def post_analysis(file_name, file_bytes, job_description):
    return client.post(
        "/analyze",
        files={"resume": (file_name, file_bytes, "application/pdf")},
        data={"job_description": job_description},
    )


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_returns_matched_and_missing_skills():
    pdf_bytes = make_pdf_bytes("Skills: Python and SQL")
    response = post_analysis("resume.pdf", pdf_bytes, JOB_TEXT)
    assert response.status_code == 200
    body = response.json()
    assert body["matched_skills"] == ["Python", "SQL"]
    assert body["missing_skills"] == ["React", "Docker"]
    assert 0 <= body["score"] <= 100


def test_non_pdf_file_is_rejected():
    response = post_analysis("resume.txt", b"hello", JOB_TEXT)
    assert response.status_code == 400


def test_invalid_pdf_is_rejected():
    response = post_analysis("resume.pdf", b"this is not a pdf", JOB_TEXT)
    assert response.status_code == 400


def test_blank_pdf_is_rejected():
    response = post_analysis("resume.pdf", make_pdf_bytes(""), JOB_TEXT)
    assert response.status_code == 400


def test_blank_job_description_is_rejected():
    response = post_analysis("resume.pdf", make_pdf_bytes("Skills: Python"), "   ")
    assert response.status_code == 400


def test_missing_job_description_returns_422():
    pdf_bytes = make_pdf_bytes("Skills: Python")
    response = client.post("/analyze", files={"resume": ("resume.pdf", pdf_bytes, "application/pdf")})
    assert response.status_code == 422