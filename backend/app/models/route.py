"""Route and RouteStop ORM models.

Route
-----
A named railway path (e.g. "Delhi–Mumbai Central via Vadodara").
Multiple train services can follow the same route on different dates.

RouteStop
---------
A junction entity that places a Station on a Route at a specific
sequence position.  The cumulative ``distance_from_origin_km`` enables
fare calculation without summing individual segment distances.

Unique constraints
------------------
- ``(route_id, stop_sequence)`` – no two stops can share the same position.
- ``(route_id, station_id)``     – a station cannot appear twice on one route.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Route(Base):
    """A named sequence of stations that one or more train services follow."""

    __tablename__ = "routes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    total_distance_km: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    # relationships
    stops: Mapped[list["RouteStop"]] = relationship(
        "RouteStop", back_populates="route", order_by="RouteStop.stop_sequence"
    )

    def __repr__(self) -> str:
        return f"<Route code={self.code!r} name={self.name!r}>"


class RouteStop(Base):
    """A station at a specific position along a route."""

    __tablename__ = "route_stops"
    __table_args__ = (
        UniqueConstraint("route_id", "stop_sequence", name="uq_route_stop_sequence"),
        UniqueConstraint("route_id", "station_id", name="uq_route_stop_station"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    route_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    station_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("stations.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    stop_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_from_origin_km: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # relationships
    route: Mapped["Route"] = relationship("Route", back_populates="stops")
    station: Mapped["Station"] = relationship("Station")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<RouteStop route={self.route_id!r} seq={self.stop_sequence}>"
