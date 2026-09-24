"""Route domain rules."""

from sqlalchemy.orm import Session

from app.api.v1.schemas import RouteCreate, RouteStopCreate
from app.models.route import Route, RouteStop
from app.models.station import Station
from app.repositories import route as route_repository


class RouteCodeAlreadyExistsError(ValueError):
    """Raised when a route code is already registered."""


class RouteStopStationNotFoundError(ValueError):
    """Raised when a route stop references an unknown station."""


def create_route(session: Session, payload: RouteCreate) -> Route:
    if route_repository.get_by_code(session, payload.code) is not None:
        raise RouteCodeAlreadyExistsError("A route with this code already exists")
    return route_repository.create(session, **payload.model_dump())


def add_stop(session: Session, route: Route, payload: RouteStopCreate) -> RouteStop:
    if session.get(Station, payload.station_id) is None:
        raise RouteStopStationNotFoundError("Station not found")
    return route_repository.create_stop(
        session, route_id=route.id, **payload.model_dump()
    )
