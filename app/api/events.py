from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.detection.engine import calculate_risk
from app.models.event import SecurityEvent
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

    if (
        event.event_type == "authentication_failure"
        and event.source_ip
    ):
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

        statement = select(func.count(SecurityEvent.id)).where(
            SecurityEvent.event_type == "authentication_failure",
            SecurityEvent.source_ip == event.source_ip,
            SecurityEvent.timestamp >= five_minutes_ago,
        )

        previous_count = db.scalar(statement) or 0
        recent_count = previous_count + 1

    risk_score, severity, detection = calculate_risk(
        event_type=event.event_type,
        username=event.username,
        recent_event_count=recent_count,
    )

    print(
        f"[DETECTION] {detection} | "
        f"Source: {event.source_ip} | "
        f"Risk: {risk_score}/100 | "
        f"Severity: {severity}"
    )

    db_event = SecurityEvent(
        **event.model_dump(),
        severity=severity,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


@router.get("/", response_model=list[SecurityEventResponse])
def get_events(db: Session = Depends(get_db)):
    statement = (
        select(SecurityEvent)
        .order_by(SecurityEvent.timestamp.desc())
        .limit(100)
    )

    return db.scalars(statement).all()