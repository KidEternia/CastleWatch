from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.api.events import router as events_router
from app.api.incidents import router as incidents_router
from app.database.database import test_database_connection


app = FastAPI(
    title="CastleWatch",
    description=(
        "Self-hosted security monitoring "
        "and incident response platform."
    ),
    version="0.1.0",
)

app.include_router(events_router)
app.include_router(incidents_router)


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