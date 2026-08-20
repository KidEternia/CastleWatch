from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.incident import Incident
from app.schemas.incident import IncidentResponse

router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[IncidentResponse])
def get_incidents(
    db: Session = Depends(get_db),
):
    statement = (
        select(Incident)
        .order_by(Incident.created_at.desc())
        .limit(100)
    )

    return db.scalars(statement).all()


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return incident


@router.post("/{incident_id}/close", response_model=IncidentResponse)
def close_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    incident.status = "closed"

    db.commit()
    db.refresh(incident)

    return incident