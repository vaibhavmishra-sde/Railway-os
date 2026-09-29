from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.db.session import Base
from app.models.route import Route, RouteStop
from app.models.seat import Seat
from app.models.service import ServiceStop, TrainService
from app.models.station import Station
from app.models.train import Coach, Train
from app.seed.network import (
    seed_coaches,
    seed_full_network,
    seed_network,
    seed_seats,
    seed_service_stops,
    seed_services,
    seed_trains,
    validate_service_stops,
)


def test_network_seed_is_idempotent():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        seed_network(session)
        seed_network(session)
        assert len(session.scalars(select(Station)).all()) == 12
        assert len(session.scalars(select(Route)).all()) == 3
        assert len(session.scalars(select(RouteStop)).all()) == 34


def test_route_stops_are_ordered_and_have_cumulative_distance():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        seed_network(session)
        route = session.scalar(select(Route).where(Route.code == "NCR-CST"))
        assert route is not None
        stops = session.scalars(
            select(RouteStop)
            .where(RouteStop.route_id == route.id)
            .order_by(RouteStop.stop_sequence)
        ).all()
        assert stops[0].distance_from_origin_km == 0
        assert stops[-1].distance_from_origin_km == route.total_distance_km


def test_train_seed_uses_service_catalog_numbers():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        trains = seed_trains(session)
        session.commit()
        assert set(trains) == {"12001", "12002", "12003", "12004", "12005"}
        assert len(session.scalars(select(Train)).all()) == 5


def test_coach_seed_gives_each_train_three_classes():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        trains = seed_trains(session)
        seed_coaches(session, trains)
        session.commit()
        assert len(session.scalars(select(Coach)).all()) == 15


def test_seat_seed_creates_expected_capacity():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        coaches = seed_coaches(session, seed_trains(session))
        seed_seats(session, coaches)
        session.commit()
        assert len(session.scalars(select(Seat)).all()) == 90


def test_service_seed_creates_dated_services_and_stops():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        stations, routes = seed_network(session)
        services = seed_services(session, seed_trains(session), routes)
        seed_service_stops(session, services)
        session.commit()
        assert len(session.scalars(select(TrainService)).all()) == 5
        assert len(session.scalars(select(ServiceStop)).all()) == 58


def test_full_seed_can_be_repeated_without_new_rows():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        first = seed_full_network(session)
        second = seed_full_network(session)
        assert first == {
            "stations": 12,
            "routes": 3,
            "trains": 5,
            "coaches": 15,
            "seats": 90,
            "services": 5,
            "stops": 58,
        }
        assert second["stations"] == 12
        assert len(session.scalars(select(ServiceStop)).all()) == 58


def test_seeded_timetable_has_valid_boundaries():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        _, routes = seed_network(session)
        services = seed_services(session, seed_trains(session), routes)
        for service in services.values():
            validate_service_stops(seed_service_stops(session, {"service": service}))
