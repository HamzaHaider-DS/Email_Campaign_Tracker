from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime
from enum import Enum


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENT = "sent"
    ARCHIVED = "archived"


class CampaignCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=1, max_length=100, description="Display name for the campaign")]
    subject: Annotated[str, Field(..., min_length=1, max_length=150, description="Subject line shown to recipients")]
    body: Annotated[str, Field(..., min_length=1, description="HTML or plain text email content")]


class CampaignUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, min_length=1, max_length=100, description="Updated campaign name")]
    subject: Annotated[Optional[str], Field(None, min_length=1, max_length=150, description="Updated email subject")]
    body: Annotated[Optional[str], Field(None, min_length=1, description="Updated email body content")]
    status: Annotated[Optional[CampaignStatus], Field(None, description="New campaign status")]


class CampaignResponse(BaseModel):
    id: int
    name: str
    subject: str
    body: str
    status: CampaignStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)