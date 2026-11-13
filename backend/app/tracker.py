"""Endpoints for the application tracker."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Analysis, Application
from app.schemas import (
    ApplicationCreate,
    ApplicationRecord,
    ApplicationStats,
    ApplicationStatus,
    ApplicationUpdate,
)

router = APIRouter(prefix="/applications", tags=["applications"])


def get_application_or_404(db: Session, application_id: int) -> Application:
    application = db.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found.")
    return application


@router.post("", response_model=ApplicationRecord, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    """Add a new application to the tracker."""
    if payload.analysis_id is not None and db.get(Analysis, payload.analysis_id) is None:
        raise HTTPException(status_code=404, detail="The linked analysis does not exist.")

    application = Application(
        job_title=payload.job_title,
        company=payload.company,
        status=payload.status.value,
        notes=payload.notes,
        analysis_id=payload.analysis_id,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("", response_model=list[ApplicationRecord])
def list_applications(
    status: ApplicationStatus | None = None,
    sort: Literal["newest", "oldest"] = Query("newest"),
    db: Session = Depends(get_db),
):
    """List applications. Optionally filter by status and sort by date."""
    query = select(Application)
    if status is not None:
        query = query.where(Application.status == status.value)

    if sort == "newest":
        query = query.order_by(Application.created_at.desc(), Application.id.desc())
    else:
        query = query.order_by(Application.created_at.asc(), Application.id.asc())

    return db.scalars(query).all()


# This route must come BEFORE "/{application_id}", otherwise "stats" would be
# treated as an id.
@router.get("/stats", response_model=ApplicationStats)
def application_stats(db: Session = Depends(get_db)):
    """Count applications in total and per status."""
    by_status = {status.value: 0 for status in ApplicationStatus}
    rows = db.execute(select(Application.status, func.count()).group_by(Application.status)).all()
    for status_value, count in rows:
        by_status[status_value] = count
    return {"total": sum(by_status.values()), "by_status": by_status}


@router.get("/{application_id}", response_model=ApplicationRecord)
def get_application(application_id: int, db: Session = Depends(get_db)):
    return get_application_or_404(db, application_id)


@router.patch("/{application_id}", response_model=ApplicationRecord)
def update_application(
    application_id: int, payload: ApplicationUpdate, db: Session = Depends(get_db)
):
    """Change only the fields that were sent (for example just the status)."""
    application = get_application_or_404(db, application_id)

    changes = payload.model_dump(exclude_unset=True, exclude_none=True, mode="json")
    for field, value in changes.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=204)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = get_application_or_404(db, application_id)
    db.delete(application)
    db.commit()
    return Response(status_code=204)