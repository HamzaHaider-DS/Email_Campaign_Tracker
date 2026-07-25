from pydantic import BaseModel
from enum import Enum


class EventType(str, Enum):
    SENT = "sent"
    OPEN = "open"
    CLICK = "click"


class EventResponse(BaseModel):
    id: int
    contact_id: int
    campaign_id: int
    type: EventType
    created_at: str
