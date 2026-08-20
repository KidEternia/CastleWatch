from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SecurityEventCreate(BaseModel):
    source_system: str
    event_type: str
    source_ip: str | None = None
    destination_ip: str | None = None
    username: str | None = None
    message: str
    raw_log: str | None = None


class SecurityEventResponse(BaseModel):
    id: int
    timestamp: datetime

    source_system: str
    event_type: str

    severity: str
    risk_score: int
    detection_name: str | None = None

    mitre_technique_id: str | None = None
    mitre_technique_name: str | None = None
    mitre_tactic: str | None = None

    source_ip: str | None = None
    destination_ip: str | None = None
    username: str | None = None

    message: str
    raw_log: str | None = None

    model_config = ConfigDict(from_attributes=True)