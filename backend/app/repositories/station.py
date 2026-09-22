"""Persistence operations for stations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.station import Station


def get_by_code(session: Session, code: str) -> Station | None:
    """Return a station by its normalized code, if present."""
    return session.scalar(select(Station).where(Station.code == code))


def list_active(session: Session) -> list[Station]:
    """Return active stations ordered for predictable public responses."""
    return list(
        session.scalars(select(Station).where(Station.is_active).order_by(Station.code))
    )


def create(session: Session, **station_data: str) -> Station:
    """Persist and refresh a station instance."""
    station = Station(**station_data)
    session.add(station)
    session.commit()
    session.refresh(station)
    return station
