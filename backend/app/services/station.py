"""Station domain rules."""

from sqlalchemy.orm import Session

from app.api.v1.schemas import StationCreate
from app.models.station import Station
from app.repositories import station as station_repository


class StationCodeAlreadyExistsError(ValueError):
    """Raised when a station code is already in the network."""


def create_station(session: Session, payload: StationCreate) -> Station:
    """Create a station while preserving code uniqueness as a domain rule."""
    if station_repository.get_by_code(session, payload.code) is not None:
        raise StationCodeAlreadyExistsError("A station with this code already exists")
    return station_repository.create(session, **payload.model_dump())
