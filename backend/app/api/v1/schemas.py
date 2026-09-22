"""Response models for version 1 endpoints."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HealthResponse(BaseModel):
    """Stable response returned when the API process is available."""

    status: Literal["ok"]
    service: str
    version: str


class StationCreate(BaseModel):
    """Validated input used to create a station."""

    code: str = Field(min_length=2, max_length=10, examples=["NDLS"])
    name: str = Field(min_length=2, max_length=200)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    timezone: str = Field(default="Asia/Kolkata", min_length=1, max_length=50)

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not normalized.isalnum():
            raise ValueError("Station code must contain letters and numbers only")
        return normalized


class StationResponse(BaseModel):
    """Public representation of a railway station."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    name: str
    city: str
    state: str
    timezone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
