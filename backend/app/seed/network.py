"""Idempotent seed operations for the synthetic station network."""

from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.network import ROUTES, SERVICES, STATIONS, validate_catalog
from app.models.identity import Role
from app.models.route import Route, RouteStop
from app.models.seat import BerthType, Seat
from app.models.service import ServiceStop, TrainService
from app.models.station import Station
from app.models.train import Coach, SeatClass, Train

TRAIN_CATALOG = {
    "12001": "Coastal Express",
    "12002": "Coastal Express Evening",
    "12003": "Harbor Link",
    "12004": "Riverside Coastal",
    "12005": "Coastal Express Return",
}
COACH_LAYOUT = (
    ("A1", SeatClass.FIRST_AC, 4),
    ("B1", SeatClass.SECOND_AC, 6),
    ("S1", SeatClass.SLEEPER, 8),
)

ROLE_CATALOG = (
    ("passenger", "Passenger"),
    ("station_staff", "Station staff"),
    ("operations_manager", "Operations manager"),
    ("admin", "Administrator"),
)


def seed_roles(session: Session) -> dict[str, Role]:
    """Create the approved authorization roles idempotently."""
    keys = [key for key, _ in ROLE_CATALOG]
    roles = {
        role.key: role
        for role in session.scalars(select(Role).where(Role.key.in_(keys)))
    }
    for key, name in ROLE_CATALOG:
        if key not in roles:
            role = Role(key=key, name=name)
            session.add(role)
            roles[key] = role
    session.flush()
    return roles


def seed_stations(session: Session) -> dict[str, Station]:
    """Insert catalog stations that are missing and return all catalog stations."""
    validate_catalog()
    codes = [item.code for item in STATIONS]
    existing = {
        station.code: station
        for station in session.scalars(select(Station).where(Station.code.in_(codes)))
    }
    for item in STATIONS:
        if item.code not in existing:
            station = Station(
                code=item.code, name=item.name, city=item.city, state=item.state
            )
            session.add(station)
            existing[item.code] = station
    session.flush()
    return existing


def seed_routes(session: Session, stations: dict[str, Station]) -> dict[str, Route]:
    """Insert missing routes and ordered stops without duplicating existing rows."""
    codes = [item.code for item in ROUTES]
    existing = {
        route.code: route
        for route in session.scalars(select(Route).where(Route.code.in_(codes)))
    }
    for item in ROUTES:
        route = existing.get(item.code)
        if route is None:
            route = Route(
                code=item.code, name=item.name, total_distance_km=item.distance_km
            )
            session.add(route)
            session.flush()
            existing[item.code] = route
        current = {
            stop.stop_sequence
            for stop in session.scalars(
                select(RouteStop).where(RouteStop.route_id == route.id)
            )
        }
        for sequence, station_code in enumerate(item.station_codes, start=1):
            if sequence not in current:
                session.add(
                    RouteStop(
                        route_id=route.id,
                        station_id=stations[station_code].id,
                        stop_sequence=sequence,
                        distance_from_origin_km=item.distance_km
                        * (sequence - 1)
                        / (len(item.station_codes) - 1),
                    )
                )
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
    existing = {
        train.number: train
        for train in session.scalars(select(Train).where(Train.number.in_(numbers)))
    }
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
                coach = Coach(
                    train_id=train.id,
                    coach_number=number,
                    seat_class=seat_class,
                    total_seats=total_seats,
                )
                session.add(coach)
                created.append(coach)
    session.flush()
    return created


def seed_seats(session: Session, coaches: list[Coach]) -> list[Seat]:
    """Create stable seat labels for newly seeded coaches."""
    created: list[Seat] = []
    for coach in coaches:
        existing = {
            seat.seat_number
            for seat in session.scalars(select(Seat).where(Seat.coach_id == coach.id))
        }
        for number in range(1, coach.total_seats + 1):
            label = str(number)
            if label not in existing:
                seat = Seat(
                    coach_id=coach.id, seat_number=label, berth_type=BerthType.SEAT
                )
                session.add(seat)
                created.append(seat)
    session.flush()
    return created


def seed_services(
    session: Session, trains: dict[str, Train], routes: dict[str, Route]
) -> dict[str, TrainService]:
    """Insert dated train services from the catalog."""
    result: dict[str, TrainService] = {}
    for item in SERVICES:
        key = f"{item.train_number}:{item.service_date}"
        service = session.scalar(
            select(TrainService)
            .join(Train)
            .where(
                Train.number == item.train_number,
                TrainService.service_date == date.fromisoformat(item.service_date),
            )
        )
        if service is None:
            service = TrainService(
                train_id=trains[item.train_number].id,
                route_id=routes[item.route_code].id,
                service_date=date.fromisoformat(item.service_date),
            )
            session.add(service)
            session.flush()
        result[key] = service
    session.flush()
    return result


def seed_service_stops(
    session: Session, services: dict[str, TrainService]
) -> list[ServiceStop]:
    """Create hourly timetable stops for each seeded service."""
    created: list[ServiceStop] = []
    for service in services.values():
        route_stops = session.scalars(
            select(RouteStop)
            .where(RouteStop.route_id == service.route_id)
            .order_by(RouteStop.stop_sequence)
        ).all()
        existing = {
            stop.stop_sequence
            for stop in session.scalars(
                select(ServiceStop).where(ServiceStop.service_id == service.id)
            )
        }
        for route_stop in route_stops:
            if route_stop.stop_sequence not in existing:
                departure = time(6 + (route_stop.stop_sequence - 1), 0)
                created.append(
                    ServiceStop(
                        service_id=service.id,
                        station_id=route_stop.station_id,
                        stop_sequence=route_stop.stop_sequence,
                        scheduled_arrival=None
                        if route_stop.stop_sequence == 1
                        else departure,
                        scheduled_departure=None
                        if route_stop.stop_sequence == len(route_stops)
                        else (
                            departure
                            if route_stop.stop_sequence == 1
                            else (time(6 + route_stop.stop_sequence, 0))
                        ),
                    )
                )
                session.add(created[-1])
    session.flush()
    return created


def seed_full_network(session: Session) -> dict[str, int]:
    """Seed the complete demo catalog and return inserted/catalog counts."""
    roles = seed_roles(session)
    stations, routes = seed_network(session)
    trains = seed_trains(session)
    coaches = seed_coaches(session, trains)
    seats = seed_seats(session, coaches)
    services = seed_services(session, trains, routes)
    stops = seed_service_stops(session, services)
    session.commit()

    return {
        "roles": len(roles),
        "stations": len(stations),
        "routes": len(routes),
        "trains": len(trains),
        "coaches": len(coaches),
        "seats": len(seats),
        "services": len(services),
        "stops": len(stops),
    }


def validate_service_stops(stops: list[ServiceStop]) -> None:
    """Reject malformed timetable boundaries before a demo seed is accepted."""
    ordered = sorted(stops, key=lambda stop: stop.stop_sequence)
    if not ordered:
        raise ValueError("a service must contain at least one stop")
    if ordered[0].scheduled_arrival is not None:
        raise ValueError("the first stop cannot have an arrival time")
    if ordered[-1].scheduled_departure is not None:
        raise ValueError("the final stop cannot have a departure time")
