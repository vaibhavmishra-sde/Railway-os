import pytest

from app.services.booking import (
    BookingStatus,
    InvalidBookingTransition,
    allowed_booking_transitions,
    transition_booking,
)


def test_booking_can_progress_through_payment_confirmation_and_completion():
    status = transition_booking(BookingStatus.DRAFT, BookingStatus.PAYMENT_PENDING)
    status = transition_booking(status, BookingStatus.CONFIRMED)
    assert transition_booking(status, BookingStatus.COMPLETED) is BookingStatus.COMPLETED


def test_failed_payment_can_retry_but_confirmed_booking_cannot_return_to_payment():
    assert transition_booking(BookingStatus.PAYMENT_PENDING, BookingStatus.PAYMENT_FAILED) is BookingStatus.PAYMENT_FAILED
    assert transition_booking(BookingStatus.PAYMENT_FAILED, BookingStatus.PAYMENT_PENDING) is BookingStatus.PAYMENT_PENDING
    with pytest.raises(InvalidBookingTransition):
        transition_booking(BookingStatus.CONFIRMED, BookingStatus.PAYMENT_PENDING)


def test_cancel_and_refund_transitions_are_explicit():
    assert transition_booking(BookingStatus.CONFIRMED, BookingStatus.CANCELLED) is BookingStatus.CANCELLED
    assert transition_booking(BookingStatus.CANCELLED, BookingStatus.REFUND_PENDING) is BookingStatus.REFUND_PENDING
    assert transition_booking(BookingStatus.REFUND_PENDING, BookingStatus.REFUNDED) is BookingStatus.REFUNDED
    assert allowed_booking_transitions(BookingStatus.REFUNDED) == frozenset()


def test_terminal_states_reject_further_transitions():
    with pytest.raises(InvalidBookingTransition):
        transition_booking(BookingStatus.EXPIRED, BookingStatus.CONFIRMED)
