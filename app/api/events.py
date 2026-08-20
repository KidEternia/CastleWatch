from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.detection.engine import calculate_risk
from app.models.event import SecurityEvent
from app.models.incident import Incident
from app.schemas.event import SecurityEventCreate, SecurityEventResponse

router = APIRouter(
    prefix="/api/events",
    tags=["Security Events"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SecurityEventResponse)
def create_event(
    event: SecurityEventCreate,
    db: Session = Depends(get_db),
):
    recent_count = 1

    if event.event_type == "authentication_failure" and event.source_ip:
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

        statement = select(func.count(SecurityEvent.id)).where(
            SecurityEvent.event_type == "authentication_failure",
            SecurityEvent.source_ip == event.source_ip,
            SecurityEvent.timestamp >= five_minutes_ago,
        )

        previous_count = db.scalar(statement) or 0
        recent_count = previous_count + 1

    (
        risk_score,
        severity,
        detection_name,
        mitre_technique_id,
        mitre_technique_name,
        mitre_tactic,
    ) = calculate_risk(
        event_type=event.event_type,
        username=event.username,
        recent_event_count=recent_count,
    )

    print(
        f"[DETECTION] {detection_name} | "
        f"Source: {event.source_ip} | "
        f"Risk: {risk_score}/100 | "
        f"Severity: {severity} | "
        f"MITRE: {mitre_technique_id or 'N/A'}"
    )

    db_event = SecurityEvent(
        **event.model_dump(),
        severity=severity,
        risk_score=risk_score,
        detection_name=detection_name,
        mitre_technique_id=mitre_technique_id,
        mitre_technique_name=mitre_technique_name,
        mitre_tactic=mitre_tactic,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    if severity in {"high", "critical"}:
        existing_incident_statement = select(Incident).where(
            Incident.status == "open",
            Incident.source_ip == event.source_ip,
            Incident.detection_name == detection_name,
        )

        existing_incident = db.scalar(existing_incident_statement)

        if existing_incident is not None:
            existing_incident.event_count += 1
            existing_incident.updated_at = datetime.utcnow()

            if severity == "critical":
                existing_incident.severity = "critical"

            db.commit()
            db.refresh(existing_incident)

            print(
                f"[INCIDENT] Updated incident #{existing_incident.id} | "
                f"Events: {existing_incident.event_count} | "
                f"Source: {event.source_ip}"
            )

        else:
            incident = Incident(
                status="open",
                severity=severity,
                title=detection_name,
                description=(
                    f"CastleWatch automatically created this incident "
                    f"from security event #{db_event.id}."
                ),
                source_ip=event.source_ip,
                destination_ip=event.destination_ip,
                event_id=db_event.id,
                event_count=1,
                detection_name=detection_name,
                mitre_technique_id=mitre_technique_id,
                mitre_technique_name=mitre_technique_name,
                mitre_tactic=mitre_tactic,
            )

            db.add(incident)
            db.commit()
            db.refresh(incident)

            print(
                f"[INCIDENT] Created incident #{incident.id} | "
                f"Event #{db_event.id} | "
                f"{detection_name} | "
                f"Severity: {severity}"
            )

    return db_event


@router.get("/", response_model=list[SecurityEventResponse])
def get_events(
    db: Session = Depends(get_db),
):
    statement = (
        select(SecurityEvent)
        .order_by(SecurityEvent.timestamp.desc())
        .limit(100)
    )

    return db.scalars(statement).all()