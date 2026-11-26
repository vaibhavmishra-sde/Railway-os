"""Per-service seat inventory and sellability state."""

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


def _now() -> datetime:
    return datetime.now(UTC)


class InventoryStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    HELD = "HELD"
    SOLD = "SOLD"
    BLOCKED = "BLOCKED"


class ServiceSeatInventory(Base):
    """One sellability record for a physical seat on a dated service."""

    __tablename__ = "service_seat_inventory"
    __table_args__ = (
        UniqueConstraint("service_id", "seat_id", name="uq_inventory_service_seat"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    service_id: Mapped[str] = mapped_column(
        ForeignKey("train_services.id", ondelete="CASCADE"), nullable=False, index=True
    )
    seat_id: Mapped[str] = mapped_column(
        ForeignKey("seats.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    booking_id: Mapped[str | None] = mapped_column(
        ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True, index=True
    )
    status: Mapped[InventoryStatus] = mapped_column(
        Enum(InventoryStatus, name="inventory_status_enum"),
        nullable=False,
        default=InventoryStatus.AVAILABLE,
    )
    held_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )
