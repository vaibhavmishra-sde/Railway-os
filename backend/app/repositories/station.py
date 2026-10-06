"""Persistence operations for stations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.station import Station


def get_by_code(session: Session, code: str) -> Station | None:
    """Return a station by its normalized code, if present."""
    return session.scalar(select(Station).where(Station.code == code))


def get_active_by_id(session: Session, station_id: str) -> Station | None:
    """Return an active station by its public identifier."""
    return session.scalar(
        select(Station).where(Station.id == station_id, Station.is_active)
    )


def list_active(
    session: Session,
    *,
    search: str | None = None,
    offset: int = 0,
    limit: int = 50,
) -> list[Station]:
    """Return active stations ordered for predictable public responses."""
    statement = select(Station).where(Station.is_active)
    if search:
        normalized_search = search.strip()
        if not normalized_search:
            return list(
                session.scalars(
                    statement.order_by(Station.code).offset(offset).limit(limit)
                )
            )
        pattern = f"%{normalized_search}%"
        statement = statement.where(
            Station.code.ilike(pattern)
            | Station.name.ilike(pattern)
            | Station.city.ilike(pattern)
        )
    statement = statement.order_by(Station.code).offset(offset).limit(limit)
    return list(session.scalars(statement))


def create(session: Session, **station_data: str) -> Station:
    """Persist and refresh a station instance."""
    station = Station(**station_data)
    session.add(station)
    session.commit()
    session.refresh(station)
    return station
