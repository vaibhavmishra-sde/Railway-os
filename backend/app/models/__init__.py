"""RailwayOS ORM models package.

Import all model modules here so that:
1. Alembic's ``target_metadata`` sees every table when generating migrations.
2. Application code can do ``from app.models import Station`` etc.

All models extend ``app.db.session.Base`` (SQLAlchemy ``DeclarativeBase``).
"""

from app.models.route import Route, RouteStop  # noqa: F401
from app.models.seat import BerthType, Seat  # noqa: F401
from app.models.service import ServiceStatus, ServiceStop, TrainService  # noqa: F401
from app.models.station import Station  # noqa: F401
from app.models.train import Coach, Train  # noqa: F401

__all__ = [
    "Station",
    "Train",
    "Coach",
    "Seat",
    "BerthType",
    "Route",
    "RouteStop",
    "TrainService",
    "ServiceStatus",
    "ServiceStop",
]
