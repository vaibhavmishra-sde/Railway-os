"""Service health endpoint."""

from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.schemas import HealthResponse
from app.core.metadata import APP_NAME, APP_VERSION
from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def health_check() -> HealthResponse:
    """Return a lightweight liveness response without external dependencies."""
    return HealthResponse(status="ok", service=APP_NAME, version=APP_VERSION)


@router.get("/ready", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def readiness_check(db: Session = Depends(get_db)) -> HealthResponse:  # noqa: B008
    """Confirm that the API process and its database dependency are available."""
    db.execute(text("SELECT 1"))
    return HealthResponse(status="ok", service=APP_NAME, version=APP_VERSION)
