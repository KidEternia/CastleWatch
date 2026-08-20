from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    status: str
    severity: str

    title: str
    description: str | None = None

    source_ip: str | None = None
    destination_ip: str | None = None

    event_id: int
    event_count: int

    detection_name: str | None = None

    mitre_technique_id: str | None = None
    mitre_technique_name: str | None = None
    mitre_tactic: str | None = None

    model_config = ConfigDict(from_attributes=True)