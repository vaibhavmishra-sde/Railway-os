from app.db.session import Base
from app.models.inventory import InventoryStatus, ServiceSeatInventory


def test_service_seat_inventory_is_registered_with_expected_statuses():
    assert ServiceSeatInventory.__tablename__ in Base.metadata.tables
    assert {status.value for status in InventoryStatus} == {
        "AVAILABLE",
        "HELD",
        "SOLD",
        "BLOCKED",
    }


def test_inventory_unique_constraint_is_service_and_seat_scoped():
    constraints = {
        constraint.name for constraint in ServiceSeatInventory.__table__.constraints
    }
    assert "uq_inventory_service_seat" in constraints


def test_booking_purchase_amounts_have_nonnegative_constraints():
    from app.models.booking import Booking, Fare, PaymentAttempt, Ticket

    assert {constraint.name for constraint in Booking.__table__.constraints} >= {
        "ck_booking_total_nonnegative"
    }
    assert {constraint.name for constraint in Ticket.__table__.constraints} >= {
        "ck_ticket_fare_nonnegative"
    }
    assert {constraint.name for constraint in Fare.__table__.constraints} >= {
        "ck_fare_amount_nonnegative"
    }
    assert {constraint.name for constraint in PaymentAttempt.__table__.constraints} >= {
        "ck_payment_amount_nonnegative"
    }
