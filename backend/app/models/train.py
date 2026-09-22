"""Train and Coach ORM models.

Train
-----
A physical trainset identified by its unique Indian Railways-style number
(e.g. ``12301`` for the Howrah Rajdhani).

Coach
-----
A single carriage attached to a train.  Each coach belongs to exactly one
seat class (``SeatClass`` enum).  The composite unique constraint on
``(train_id, coach_number)`` prevents duplicate coach labels on the same train.
"""

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _now() -> datetime:
    return datetime.now(UTC)


class SeatClass(str, enum.Enum):
    """Passenger class for a coach."""

    FIRST_AC = "FIRST_AC"
    SECOND_AC = "SECOND_AC"
    THIRD_AC = "THIRD_AC"
    SLEEPER = "SLEEPER"
    GENERAL = "GENERAL"


class Train(Base):
    """A trainset that can be scheduled on one or more dated services."""

    __tablename__ = "trains"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    number: Mapped[str] = mapped_column(
        String(10), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    # relationships
    coaches: Mapped[list["Coach"]] = relationship("Coach", back_populates="train")

    def __repr__(self) -> str:
        return f"<Train number={self.number!r} name={self.name!r}>"


class Coach(Base):
    """A single carriage belonging to a train with an assigned seat class."""

    __tablename__ = "coaches"
    __table_args__ = (
        UniqueConstraint("train_id", "coach_number", name="uq_coach_train_number"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    train_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("trains.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    coach_number: Mapped[str] = mapped_column(String(10), nullable=False)
    seat_class: Mapped[SeatClass] = mapped_column(
        Enum(SeatClass, name="seat_class_enum"), nullable=False
    )
    total_seats: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # relationships
    train: Mapped["Train"] = relationship("Train", back_populates="coaches")
    seats: Mapped[list] = relationship("Seat", back_populates="coach")

    def __repr__(self) -> str:
        return f"<Coach number={self.coach_number!r} class={self.seat_class.value}>"
