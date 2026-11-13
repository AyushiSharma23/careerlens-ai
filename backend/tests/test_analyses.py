import pymupdf
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# A separate in-memory database, so tests never touch the real careerlens.db file.
test_engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

client = TestClient(app)

JOB_TEXT = "We need an intern with Python, SQL, React and Docker."


@pytest.fixture(autouse=True)
def fresh_database():
    """Give every test an empty database."""
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


def make_pdf_bytes(text):
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def save(job_title="Backend Intern", company="Acme", job_description=JOB_TEXT):
    return client.post(
        "/analyses",
        files={"resume": ("resume.pdf", make_pdf_bytes("Skills: Python and SQL"), "application/pdf")},
        data={"job_title": job_title, "company": company, "job_description": job_description},
    )


def test_saving_an_analysis_returns_201_and_the_record():
    response = save()
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["job_title"] == "Backend Intern"
    assert body["matched_skills"] == ["Python", "SQL"]
    assert body["missing_skills"] == ["React", "Docker"]


def test_saved_analyses_are_listed_newest_first():
    save(job_title="First job")
    save(job_title="Second job")
    titles = [item["job_title"] for item in client.get("/analyses").json()]
    assert titles == ["Second job", "First job"]


def test_get_one_analysis():
    saved_id = save().json()["id"]
    response = client.get(f"/analyses/{saved_id}")
    assert response.status_code == 200
    assert response.json()["job_title"] == "Backend Intern"


def test_unknown_analysis_returns_404():
    assert client.get("/analyses/999").status_code == 404
    assert client.delete("/analyses/999").status_code == 404


def test_delete_removes_the_analysis():
    saved_id = save().json()["id"]
    assert client.delete(f"/analyses/{saved_id}").status_code == 204
    assert client.get("/analyses").json() == []


def test_blank_job_title_is_rejected():
    assert save(job_title="   ").status_code == 400


def test_invalid_input_saves_nothing():
    response = save(job_description="   ")
    assert response.status_code == 400
    assert client.get("/analyses").json() == []