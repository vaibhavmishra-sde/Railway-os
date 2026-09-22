"""TrainService and ServiceStop ORM models.

TrainService
------------
A dated instance of a specific Train running a specific Route.
The unique constraint on ``(train_id, service_date)`` prevents
the same physical trainset from being scheduled twice on the same day.

ServiceStop
-----------
The scheduled call times (arrival/departure) for each station visited
by a TrainService.  The ``scheduled_arrival`` is NULL for the origin
station and ``scheduled_departure`` is NULL for the terminus.
"""

import enum
import uuid
from datetime import UTC, date, datetime, time
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.route import Route
    from app.models.station import Station
    from app.models.train import Train


def _now() -> datetime:
    return datetime.now(UTC)


class ServiceStatus(str, enum.Enum):
    """Lifecycle status of a dated train service."""

    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TrainService(Base):
    """A specific train running a route on a particular date."""

    __tablename__ = "train_services"
    __table_args__ = (
        UniqueConstraint("train_id", "service_date", name="uq_service_train_date"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    train_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("trains.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    route_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("routes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    service_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    status: Mapped[ServiceStatus] = mapped_column(
        Enum(ServiceStatus, name="service_status_enum"),
        nullable=False,
        default=ServiceStatus.SCHEDULED,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    # relationships
    train: Mapped["Train"] = relationship("Train")  # type: ignore[name-defined]
    route: Mapped["Route"] = relationship("Route")  # type: ignore[name-defined]
    service_stops: Mapped[list["ServiceStop"]] = relationship(
        "ServiceStop", back_populates="service", order_by="ServiceStop.stop_sequence"
    )

    def __repr__(self) -> str:
        return f"<TrainService train={self.train_id!r} date={self.service_date}>"


class ServiceStop(Base):
    """Scheduled arrival/departure times for one station on a TrainService."""

    __tablename__ = "service_stops"
    __table_args__ = (
        UniqueConstraint(
            "service_id", "stop_sequence", name="uq_service_stop_sequence"
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    service_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("train_services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    station_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("stations.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    stop_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    scheduled_arrival: Mapped[time | None] = mapped_column(Time, nullable=True)
    scheduled_departure: Mapped[time | None] = mapped_column(Time, nullable=True)
    platform_number: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # relationships
    service: Mapped["TrainService"] = relationship(
        "TrainService", back_populates="service_stops"
    )
    station: Mapped["Station"] = relationship("Station")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<ServiceStop service={self.service_id!r} seq={self.stop_sequence}>"
