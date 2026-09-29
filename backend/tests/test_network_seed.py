from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.db.session import Base
from app.models.route import Route, RouteStop
from app.models.station import Station
from app.seed.network import seed_network


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
        stops = session.scalars(select(RouteStop).where(RouteStop.route_id == route.id).order_by(RouteStop.stop_sequence)).all()
        assert stops[0].distance_from_origin_km == 0
        assert stops[-1].distance_from_origin_km == route.total_distance_km
