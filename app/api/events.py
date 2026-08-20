from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
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
    db_event = SecurityEvent(**event.model_dump())

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

    events = db.scalars(statement).all()

    return events