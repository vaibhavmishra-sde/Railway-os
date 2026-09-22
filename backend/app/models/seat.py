"""Seat ORM model.

A Seat is an individual berth or seat position within a Coach.
The composite unique constraint on ``(coach_id, seat_number)`` guarantees
no duplicate seat labels within the same coach.
"""

import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.train import Coach


class BerthType(str, enum.Enum):
    """Physical berth/seat arrangement within a coach."""

    LOWER = "LOWER"
    MIDDLE = "MIDDLE"
    UPPER = "UPPER"
    SIDE_LOWER = "SIDE_LOWER"
    SIDE_UPPER = "SIDE_UPPER"
    SEAT = "SEAT"  # used for chair-car / general class


class Seat(Base):
    """An individual seat or berth position within a coach."""

    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint("coach_id", "seat_number", name="uq_seat_coach_number"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    coach_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("coaches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    seat_number: Mapped[str] = mapped_column(String(10), nullable=False)
    berth_type: Mapped[BerthType] = mapped_column(
        Enum(BerthType, name="berth_type_enum"), nullable=False, default=BerthType.SEAT
    )

    # relationships
    coach: Mapped["Coach"] = relationship("Coach", back_populates="seats")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Seat seat_number={self.seat_number!r} berth={self.berth_type.value}>"
