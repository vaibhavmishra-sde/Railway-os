"""Idempotent seed operations for the synthetic station network."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.network import ROUTES, SERVICES, STATIONS, validate_catalog
from app.models.route import Route, RouteStop
from app.models.station import Station
from app.models.train import Coach, SeatClass, Train


TRAIN_CATALOG = {
    "12001": "Coastal Express",
    "12002": "Coastal Express Evening",
    "12003": "Harbor Link",
    "12004": "Riverside Coastal",
    "12005": "Coastal Express Return",
}
COACH_LAYOUT = (("A1", SeatClass.FIRST_AC, 4), ("B1", SeatClass.SECOND_AC, 6), ("S1", SeatClass.SLEEPER, 8))


def seed_stations(session: Session) -> dict[str, Station]:
    """Insert catalog stations that are missing and return all catalog stations."""
    validate_catalog()
    codes = [item.code for item in STATIONS]
    existing = {station.code: station for station in session.scalars(select(Station).where(Station.code.in_(codes)))}
    for item in STATIONS:
        if item.code not in existing:
            station = Station(code=item.code, name=item.name, city=item.city, state=item.state)
            session.add(station)
            existing[item.code] = station
    session.flush()
    return existing


def seed_routes(session: Session, stations: dict[str, Station]) -> dict[str, Route]:
    """Insert missing routes and ordered stops without duplicating existing rows."""
    codes = [item.code for item in ROUTES]
    existing = {route.code: route for route in session.scalars(select(Route).where(Route.code.in_(codes)))}
    for item in ROUTES:
        route = existing.get(item.code)
        if route is None:
            route = Route(code=item.code, name=item.name, total_distance_km=item.distance_km)
            session.add(route)
            session.flush()
            existing[item.code] = route
        current = {stop.stop_sequence for stop in session.scalars(select(RouteStop).where(RouteStop.route_id == route.id))}
        for sequence, station_code in enumerate(item.station_codes, start=1):
            if sequence not in current:
                session.add(RouteStop(
                    route_id=route.id,
                    station_id=stations[station_code].id,
                    stop_sequence=sequence,
                    distance_from_origin_km=item.distance_km * (sequence - 1) / (len(item.station_codes) - 1),
                ))
    session.flush()
    return existing


def seed_network(session: Session) -> tuple[dict[str, Station], dict[str, Route]]:
    """Seed stations and routes in one transaction managed by the caller."""
    stations = seed_stations(session)
    routes = seed_routes(session, stations)
    session.commit()
    return stations, routes


def seed_trains(session: Session) -> dict[str, Train]:
    """Insert the trains referenced by the synthetic service catalog."""
    numbers = [item.train_number for item in SERVICES]
    existing = {train.number: train for train in session.scalars(select(Train).where(Train.number.in_(numbers)))}
    for number in numbers:
        if number not in existing:
            train = Train(number=number, name=TRAIN_CATALOG[number])
            session.add(train)
            existing[number] = train
    session.flush()
    return existing


def seed_coaches(session: Session, trains: dict[str, Train]) -> list[Coach]:
    """Give every seeded train a deterministic coach layout."""
    created: list[Coach] = []
    for train in trains.values():
        existing = {coach.coach_number for coach in train.coaches}
        for number, seat_class, total_seats in COACH_LAYOUT:
            if number not in existing:
                coach = Coach(train_id=train.id, coach_number=number, seat_class=seat_class, total_seats=total_seats)
                session.add(coach)
                created.append(coach)
    session.flush()
    return created
