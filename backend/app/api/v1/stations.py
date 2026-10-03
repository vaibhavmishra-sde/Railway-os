"""Public station endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.schemas import StationCreate, StationResponse
from app.db.session import get_db
from app.repositories.station import get_active_by_id, list_active
from app.services.station import StationCodeAlreadyExistsError, create_station

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("", response_model=list[StationResponse])
def list_stations(
    search: str | None = Query(default=None, min_length=2, max_length=100),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),  # noqa: B008
) -> list[StationResponse]:
    """List active stations with optional search and pagination."""
    return list_active(db, search=search, offset=offset, limit=limit)


@router.get("/{station_id}", response_model=StationResponse)
def get_station(station_id: str, db: Session = Depends(get_db)) -> StationResponse:  # noqa: B008
    """Return one active station or a useful 404 response."""
    station = get_active_by_id(db, station_id)
    if station is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Station not found"
        )
    return station


@router.post("", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
def create_station_endpoint(
    payload: StationCreate,
    db: Session = Depends(get_db),  # noqa: B008
) -> StationResponse:
    """Create a synthetic-network station."""
    try:
        return create_station(db, payload)
    except StationCodeAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
