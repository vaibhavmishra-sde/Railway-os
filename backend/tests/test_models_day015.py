"""Smoke tests: ensure all Day 15 models can be imported and their tables exist.

These tests do NOT hit a running PostgreSQL database.  They use the
in-memory SQLite engine from conftest to exercise:
1. Python-level import and attribute access.
2. SQLAlchemy metadata creation (DDL).
"""


# ---------------------------------------------------------------------------
# Import smoke tests
# ---------------------------------------------------------------------------


def test_station_model_importable():
    """Station can be imported and has expected attributes."""
    from app.models.station import Station

    assert hasattr(Station, "__tablename__")
    assert Station.__tablename__ == "stations"
    assert hasattr(Station, "code")
    assert hasattr(Station, "timezone")


def test_train_model_importable():
    """Train and Coach can be imported; SeatClass enum has expected values."""
    from app.models.train import Coach, SeatClass, Train

    assert Train.__tablename__ == "trains"
    assert Coach.__tablename__ == "coaches"
    assert SeatClass.FIRST_AC.value == "FIRST_AC"
    assert SeatClass.SLEEPER.value == "SLEEPER"


def test_seat_model_importable():
    """Seat and BerthType can be imported; berth types are complete."""
    from app.models.seat import BerthType, Seat

    assert Seat.__tablename__ == "seats"
    expected_berths = {"LOWER", "MIDDLE", "UPPER", "SIDE_LOWER", "SIDE_UPPER", "SEAT"}
    assert {b.value for b in BerthType} == expected_berths


def test_route_models_importable():
    """Route and RouteStop can be imported with correct table names."""
    from app.models.route import Route, RouteStop

    assert Route.__tablename__ == "routes"
    assert RouteStop.__tablename__ == "route_stops"
    assert hasattr(RouteStop, "stop_sequence")
    assert hasattr(RouteStop, "distance_from_origin_km")


def test_service_models_importable():
    """TrainService and ServiceStop can be imported; ServiceStatus is complete."""
    from app.models.service import ServiceStatus, ServiceStop, TrainService

    assert TrainService.__tablename__ == "train_services"
    assert ServiceStop.__tablename__ == "service_stops"
    expected_statuses = {"SCHEDULED", "RUNNING", "COMPLETED", "CANCELLED"}
    assert {s.value for s in ServiceStatus} == expected_statuses


# ---------------------------------------------------------------------------
# DDL creation tests (uses in-memory SQLite from conftest)
# ---------------------------------------------------------------------------


def test_all_model_tables_created(test_engine):
    """All Day 15 model tables are present in the in-memory database."""
    from sqlalchemy import inspect

    inspector = inspect(test_engine)
    table_names = set(inspector.get_table_names())

    expected_tables = {
        "stations",
        "trains",
        "coaches",
        "seats",
        "routes",
        "route_stops",
        "train_services",
        "service_stops",
    }
    missing = expected_tables - table_names
    assert not missing, f"Missing tables in test DB: {missing}"


def test_station_columns(test_engine):
    """Station table has all expected columns."""
    from sqlalchemy import inspect

    cols = {c["name"] for c in inspect(test_engine).get_columns("stations")}
    assert {"id", "code", "name", "city", "state", "timezone", "is_active"} <= cols


def test_coach_unique_constraint(test_engine):
    """Coach table declares a unique constraint on (train_id, coach_number)."""
    from sqlalchemy import inspect

    uqs = inspect(test_engine).get_unique_constraints("coaches")
    uq_col_sets = [set(u["column_names"]) for u in uqs]
    assert {"train_id", "coach_number"} in uq_col_sets


def test_route_stop_unique_constraints(test_engine):
    """RouteStop table has both unique constraints."""
    from sqlalchemy import inspect

    uqs = inspect(test_engine).get_unique_constraints("route_stops")
    uq_col_sets = [set(u["column_names"]) for u in uqs]
    assert {"route_id", "stop_sequence"} in uq_col_sets
    assert {"route_id", "station_id"} in uq_col_sets
