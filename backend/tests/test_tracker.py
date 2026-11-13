import pymupdf
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_database():
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


def add_application(job_title="Backend Intern", **extra):
    return client.post("/applications", json={"job_title": job_title, **extra})


def save_analysis():
    document = pymupdf.open()
    document.new_page().insert_text((72, 72), "Skills: Python")
    pdf_bytes = document.tobytes()
    document.close()
    return client.post(
        "/analyses",
        files={"resume": ("resume.pdf", pdf_bytes, "application/pdf")},
        data={"job_title": "Backend Intern", "job_description": "Need Python and SQL."},
    ).json()["id"]


def test_new_application_defaults_to_interested():
    response = add_application(company="Acme")
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "Interested"
    assert body["company"] == "Acme"
    assert body["analysis_id"] is None


def test_invalid_status_is_rejected():
    assert add_application(status="Hired").status_code == 422


def test_blank_job_title_is_rejected():
    assert add_application(job_title="   ").status_code == 422


def test_application_can_link_to_a_saved_analysis():
    analysis_id = save_analysis()
    response = add_application(analysis_id=analysis_id)
    assert response.status_code == 201
    assert response.json()["analysis_id"] == analysis_id


def test_linking_to_unknown_analysis_returns_404():
    assert add_application(analysis_id=999).status_code == 404


def test_list_is_newest_first_and_can_be_reversed():
    add_application("First")
    add_application("Second")
    newest = [a["job_title"] for a in client.get("/applications").json()]
    oldest = [a["job_title"] for a in client.get("/applications?sort=oldest").json()]
    assert newest == ["Second", "First"]
    assert oldest == ["First", "Second"]


def test_list_can_be_filtered_by_status():
    add_application("A", status="Applied")
    add_application("B", status="Interview")
    add_application("C", status="Applied")
    titles = [a["job_title"] for a in client.get("/applications?status=Applied").json()]
    assert sorted(titles) == ["A", "C"]


def test_invalid_filter_or_sort_value_returns_422():
    assert client.get("/applications?status=Hired").status_code == 422
    assert client.get("/applications?sort=random").status_code == 422


def test_update_changes_only_the_fields_sent():
    application_id = add_application(company="Acme").json()["id"]
    response = client.patch(f"/applications/{application_id}", json={"status": "Applied"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "Applied"
    assert body["company"] == "Acme"
    assert body["job_title"] == "Backend Intern"


def test_update_with_invalid_status_is_rejected():
    application_id = add_application().json()["id"]
    response = client.patch(f"/applications/{application_id}", json={"status": "Hired"})
    assert response.status_code == 422


def test_unknown_application_returns_404():
    assert client.get("/applications/999").status_code == 404
    assert client.patch("/applications/999", json={"status": "Offer"}).status_code == 404
    assert client.delete("/applications/999").status_code == 404


def test_delete_removes_the_application():
    application_id = add_application().json()["id"]
    assert client.delete(f"/applications/{application_id}").status_code == 204
    assert client.get("/applications").json() == []


def test_stats_count_every_status_including_zeros():
    add_application("A", status="Applied")
    add_application("B", status="Applied")
    add_application("C", status="Offer")
    stats = client.get("/applications/stats").json()
    assert stats["total"] == 3
    assert stats["by_status"] == {
        "Interested": 0,
        "Applied": 2,
        "Interview": 0,
        "Offer": 1,
        "Rejected": 0,
    }


def test_deleting_an_analysis_keeps_the_application():
    analysis_id = save_analysis()
    application_id = add_application(analysis_id=analysis_id).json()["id"]
    assert client.delete(f"/analyses/{analysis_id}").status_code == 204
    body = client.get(f"/applications/{application_id}").json()
    assert body["analysis_id"] is None