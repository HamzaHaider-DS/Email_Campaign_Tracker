from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Annotated
from datetime import datetime


class ContactCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=1, max_length=100, description="Contact's full name")]
    email: Annotated[EmailStr, Field(..., description="A valid recipient email address")]

    @field_validator('name')
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().title()


class ContactResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    campaign_id: int
    tracking_token: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)