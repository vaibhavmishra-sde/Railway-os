"""Create dated service seat inventory and booking value constraints."""

import sqlalchemy as sa
from alembic import op

revision = "20261126_02"
down_revision = "20261126_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_booking_total_nonnegative", "bookings", "total_amount_minor >= 0"
    )
    op.create_check_constraint(
        "ck_ticket_fare_nonnegative", "tickets", "fare_amount_minor >= 0"
    )
    op.create_check_constraint(
        "ck_fare_amount_nonnegative", "fares", "amount_minor >= 0"
    )
    op.create_check_constraint(
        "ck_payment_amount_nonnegative", "payment_attempts", "amount_minor >= 0"
    )
    inventory_status = sa.Enum(
        "AVAILABLE", "HELD", "SOLD", "BLOCKED", name="inventory_status_enum"
    )
    inventory_status.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "service_seat_inventory",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("service_id", sa.String(36), nullable=False),
        sa.Column("seat_id", sa.String(36), nullable=False),
        sa.Column("booking_id", sa.String(36), nullable=True),
        sa.Column("status", inventory_status, nullable=False),
        sa.Column("held_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["service_id"], ["train_services.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["seat_id"], ["seats.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("service_id", "seat_id", name="uq_inventory_service_seat"),
    )
    op.create_index("ix_inventory_service_id", "service_seat_inventory", ["service_id"])
    op.create_index("ix_inventory_seat_id", "service_seat_inventory", ["seat_id"])
    op.create_index("ix_inventory_booking_id", "service_seat_inventory", ["booking_id"])


def downgrade() -> None:
    op.drop_index("ix_inventory_booking_id", table_name="service_seat_inventory")
    op.drop_index("ix_inventory_seat_id", table_name="service_seat_inventory")
    op.drop_index("ix_inventory_service_id", table_name="service_seat_inventory")
    op.drop_table("service_seat_inventory")
    sa.Enum(name="inventory_status_enum").drop(op.get_bind(), checkfirst=True)
    op.drop_constraint(
        "ck_payment_amount_nonnegative", "payment_attempts", type_="check"
    )
    op.drop_constraint("ck_fare_amount_nonnegative", "fares", type_="check")
    op.drop_constraint("ck_ticket_fare_nonnegative", "tickets", type_="check")
    op.drop_constraint("ck_booking_total_nonnegative", "bookings", type_="check")
