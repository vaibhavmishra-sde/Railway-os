"""Booking lifecycle rules shared by booking commands and persistence code."""

from enum import StrEnum


class BookingStatus(StrEnum):
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


class InvalidBookingTransition(ValueError):
    """Raised when a booking attempts a transition outside its lifecycle."""


_ALLOWED_TRANSITIONS: dict[BookingStatus, frozenset[BookingStatus]] = {
    BookingStatus.DRAFT: frozenset({BookingStatus.PAYMENT_PENDING}),
    BookingStatus.PAYMENT_PENDING: frozenset(
        {BookingStatus.CONFIRMED, BookingStatus.PAYMENT_FAILED, BookingStatus.EXPIRED}
    ),
    BookingStatus.PAYMENT_FAILED: frozenset({BookingStatus.PAYMENT_PENDING}),
    BookingStatus.CONFIRMED: frozenset(
        {BookingStatus.CANCELLED, BookingStatus.COMPLETED}
    ),
    BookingStatus.CANCELLED: frozenset({BookingStatus.REFUND_PENDING}),
    BookingStatus.REFUND_PENDING: frozenset(
        {BookingStatus.REFUNDED, BookingStatus.REFUND_FAILED}
    ),
    BookingStatus.REFUND_FAILED: frozenset({BookingStatus.REFUND_PENDING}),
    BookingStatus.REFUNDED: frozenset(),
    BookingStatus.EXPIRED: frozenset(),
    BookingStatus.COMPLETED: frozenset(),
}


def allowed_booking_transitions(status: BookingStatus) -> frozenset[BookingStatus]:
    """Return the immutable set of states reachable from ``status``."""
    return _ALLOWED_TRANSITIONS[status]


def transition_booking(status: BookingStatus, target: BookingStatus) -> BookingStatus:
    """Validate and return a booking's next state."""
    if target not in allowed_booking_transitions(status):
        raise InvalidBookingTransition(f"Cannot transition booking from {status} to {target}")
    return target
