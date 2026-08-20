from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.api.events import router as events_router
from app.database.database import Base, engine, test_database_connection
from app.models.event import SecurityEvent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CastleWatch",
    description="Self-hosted security monitoring and incident response platform.",
    version="0.1.0",
)

app.include_router(events_router)


@app.get("/")
def root():
    return {
        "name": "CastleWatch",
        "version": "0.1.0",
        "status": "online",
    }


@app.get("/health")
def health():
    try:
        test_database_connection()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except SQLAlchemyError:
        return {
            "status": "degraded",
            "database": "disconnected",
        }