"""Persistence operations for routes and their ordered stops."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.route import Route, RouteStop


def get_by_code(session: Session, code: str) -> Route | None:
    return session.scalar(select(Route).where(Route.code == code))


def get(session: Session, route_id: str) -> Route | None:
    return session.get(Route, route_id)


def list_active(session: Session) -> list[Route]:
    return list(
        session.scalars(select(Route).where(Route.is_active).order_by(Route.code))
    )


def list_stops(session: Session, route_id: str) -> list[RouteStop]:
    statement = (
        select(RouteStop)
        .where(RouteStop.route_id == route_id)
        .order_by(RouteStop.stop_sequence)
    )
    return list(session.scalars(statement))


def create(session: Session, **route_data: object) -> Route:
    route = Route(**route_data)
    session.add(route)
    session.commit()
    session.refresh(route)
    return route


def create_stop(session: Session, **stop_data: object) -> RouteStop:
    stop = RouteStop(**stop_data)
    session.add(stop)
    session.commit()
    session.refresh(stop)
    return stop
