"""Public station endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.schemas import StationCreate, StationResponse
from app.db.session import get_db
from app.repositories.station import list_active
from app.services.station import StationCodeAlreadyExistsError, create_station

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("", response_model=list[StationResponse])
def list_stations(db: Session = Depends(get_db)) -> list[StationResponse]:
    """List active stations in station-code order."""
    return list_active(db)


@router.post("", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
def create_station_endpoint(
    payload: StationCreate, db: Session = Depends(get_db)
) -> StationResponse:
    """Create a synthetic-network station."""
    try:
        return create_station(db, payload)
    except StationCodeAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
