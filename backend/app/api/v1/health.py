"""Service health endpoint."""

from fastapi import APIRouter, status

from app.api.v1.schemas import HealthResponse
from app.core.metadata import APP_NAME, APP_VERSION

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def health_check() -> HealthResponse:
    """Return a lightweight liveness response without external dependencies."""
    return HealthResponse(status="ok", service=APP_NAME, version=APP_VERSION)
