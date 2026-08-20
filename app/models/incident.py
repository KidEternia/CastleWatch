from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    destination_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    event_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    event_count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    detection_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    mitre_technique_id: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    mitre_technique_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    mitre_tactic: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )