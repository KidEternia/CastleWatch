from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SecurityEventCreate(BaseModel):
    source_system: str
    event_type: str
    severity: str
    source_ip: str | None = None
    destination_ip: str | None = None
    username: str | None = None
    message: str
    raw_log: str | None = None


class SecurityEventResponse(SecurityEventCreate):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)