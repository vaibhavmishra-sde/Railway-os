"""Response models for version 1 endpoints."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.train import SeatClass


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


class TrainCreate(BaseModel):
    """Validated input for a trainset."""

    number: str = Field(min_length=5, max_length=10, examples=["12301"])
    name: str = Field(min_length=2, max_length=200)

    @field_validator("number")
    @classmethod
    def normalize_number(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized.isdigit():
            raise ValueError("Train number must contain digits only")
        return normalized


class CoachCreate(BaseModel):
    """Validated input for a coach attached to a train."""

    coach_number: str = Field(min_length=1, max_length=10, examples=["A1"])
    seat_class: SeatClass
    total_seats: int = Field(ge=1, le=200)

    @field_validator("coach_number")
    @classmethod
    def normalize_coach_number(cls, value: str) -> str:
        return value.strip().upper()


class TrainResponse(BaseModel):
    """Public trainset representation."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    number: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CoachResponse(BaseModel):
    """Public representation of one coach in a trainset."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    train_id: str
    coach_number: str
    seat_class: SeatClass
    total_seats: int


class RouteCreate(BaseModel):
    """Validated input for a named synthetic railway route."""

    code: str = Field(min_length=2, max_length=20, examples=["NDLS-BCT"])
    name: str = Field(min_length=2, max_length=200)
    total_distance_km: float = Field(ge=0, le=10_000)

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not all(character.isalnum() or character == "-" for character in normalized):
            raise ValueError("Route code may contain letters, numbers, and hyphens only")
        return normalized


class RouteStopCreate(BaseModel):
    """A station's ordered position along a route."""

    station_id: str
    stop_sequence: int = Field(ge=1)
    distance_from_origin_km: float = Field(ge=0, le=10_000)


class RouteResponse(BaseModel):
    """Public representation of a route."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    name: str
    total_distance_km: float
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RouteStopResponse(BaseModel):
    """Public representation of one route stop."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    route_id: str
    station_id: str
    stop_sequence: int
    distance_from_origin_km: float
