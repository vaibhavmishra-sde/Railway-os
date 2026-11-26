"""Booking aggregate models for passenger purchase records."""

import enum
import uuid
from datetime import UTC, date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


def _now() -> datetime:
    return datetime.now(UTC)


class BookingStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    REFUND_PENDING = "REFUND_PENDING"
    REFUNDED = "REFUNDED"
    REFUND_FAILED = "REFUND_FAILED"
    EXPIRED = "EXPIRED"
    COMPLETED = "COMPLETED"


class PaymentAttemptStatus(str, enum.Enum):
    CREATED = "CREATED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("pnr", name="uq_booking_pnr"),
        UniqueConstraint("user_id", "idempotency_key", name="uq_booking_idempotency"),
        CheckConstraint("total_amount_minor >= 0", name="ck_booking_total_nonnegative"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    pnr: Mapped[str | None] = mapped_column(String(10), nullable=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    service_id: Mapped[str] = mapped_column(
        ForeignKey("train_services.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status_enum"),
        nullable=False,
        default=BookingStatus.DRAFT,
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    total_amount_minor: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    idempotency_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )


class Traveller(Base):
    __tablename__ = "travellers"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    booking_id: Mapped[str] = mapped_column(
        ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    identity_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        CheckConstraint("fare_amount_minor >= 0", name="ck_ticket_fare_nonnegative"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    booking_id: Mapped[str] = mapped_column(
        ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    traveller_id: Mapped[str] = mapped_column(
        ForeignKey("travellers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    seat_id: Mapped[str | None] = mapped_column(
        ForeignKey("seats.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    boarding_station_id: Mapped[str] = mapped_column(
        ForeignKey("stations.id", ondelete="RESTRICT"), nullable=False
    )
    arrival_station_id: Mapped[str] = mapped_column(
        ForeignKey("stations.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="HELD")
    fare_amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)


class Fare(Base):
    __tablename__ = "fares"
    __table_args__ = (
        UniqueConstraint("booking_id", "seat_class", name="uq_fare_booking_class"),
        CheckConstraint("amount_minor >= 0", name="ck_fare_amount_nonnegative"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    booking_id: Mapped[str] = mapped_column(
        ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    seat_class: Mapped[str] = mapped_column(String(30), nullable=False)
    amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")


class PaymentAttempt(Base):
    __tablename__ = "payment_attempts"
    __table_args__ = (
        CheckConstraint("amount_minor >= 0", name="ck_payment_amount_nonnegative"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    booking_id: Mapped[str] = mapped_column(
        ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider: Mapped[str] = mapped_column(
        String(50), nullable=False, default="SIMULATED"
    )
    status: Mapped[PaymentAttemptStatus] = mapped_column(
        Enum(PaymentAttemptStatus, name="payment_attempt_status_enum"),
        nullable=False,
        default=PaymentAttemptStatus.CREATED,
    )
    amount_minor: Mapped[int] = mapped_column(Integer, nullable=False)
    provider_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
