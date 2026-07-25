from datetime import datetime
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserCreate(BaseModel):
    email: Annotated[EmailStr, Field(..., description="A valid email address for the new account")]
    password: Annotated[
        str,
        Field(
            ...,
            min_length=8,
            description="Password must be at least 8 characters long and contain at least one number",
        ),
    ]

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(..., description="The email used during registration")]
    password: Annotated[str, Field(..., description="The account password")]


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    created_at: datetime  # <--- Changed from str to datetime

    # Configures Pydantic v2 to read attributes directly from SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)