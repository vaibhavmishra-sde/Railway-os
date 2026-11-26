from app.db.session import Base
from app.models.booking import (
    Booking,
    BookingStatus,
    Fare,
    PaymentAttempt,
    PaymentAttemptStatus,
    Ticket,
    Traveller,
)


def test_booking_purchase_tables_are_registered():
    assert {
        Booking.__tablename__,
        Traveller.__tablename__,
        Ticket.__tablename__,
        Fare.__tablename__,
        PaymentAttempt.__tablename__,
    } <= set(Base.metadata.tables)


def test_booking_status_defaults_match_lifecycle_design():
    assert BookingStatus.DRAFT.value == "DRAFT"
    assert PaymentAttemptStatus.CREATED.value == "CREATED"
    assert Booking.__table__.c.currency.default.arg == "INR"
    assert PaymentAttempt.__table__.c.provider.default.arg == "SIMULATED"


def test_booking_has_purchase_record_constraints():
    constraint_names = {constraint.name for constraint in Booking.__table__.constraints}
    assert "uq_booking_pnr" in constraint_names
    assert "uq_booking_idempotency" in constraint_names
    assert "uq_fare_booking_class" in {
        constraint.name for constraint in Fare.__table__.constraints
    }
