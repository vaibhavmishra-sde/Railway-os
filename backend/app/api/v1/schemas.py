"""Response models for version 1 endpoints."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Stable response returned when the API process is available."""

    status: Literal["ok"]
    service: str
    version: str
