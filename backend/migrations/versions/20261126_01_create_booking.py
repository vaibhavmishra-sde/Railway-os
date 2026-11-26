"""Create booking purchase-record tables."""

import sqlalchemy as sa
from alembic import op

revision = "20261126_01"
down_revision = "20261005_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    booking_status = sa.Enum(
        "DRAFT",
        "PAYMENT_PENDING",
        "PAYMENT_FAILED",
        "CONFIRMED",
        "CANCELLED",
        "REFUND_PENDING",
        "REFUNDED",
        "REFUND_FAILED",
        "EXPIRED",
        "COMPLETED",
        name="booking_status_enum",
    )
    payment_status = sa.Enum(
        "CREATED", "SUCCEEDED", "FAILED", name="payment_attempt_status_enum"
    )
    booking_status.create(op.get_bind(), checkfirst=True)
    payment_status.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "bookings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("pnr", sa.String(10), nullable=True),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("service_id", sa.String(36), nullable=False),
        sa.Column("status", booking_status, nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("total_amount_minor", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(100), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["service_id"], ["train_services.id"], ondelete="RESTRICT"
        ),
        sa.UniqueConstraint("pnr", name="uq_booking_pnr"),
        sa.UniqueConstraint(
            "user_id", "idempotency_key", name="uq_booking_idempotency"
        ),
    )
    op.create_index("ix_bookings_user_id", "bookings", ["user_id"])
    op.create_index("ix_bookings_service_id", "bookings", ["service_id"])
    op.create_table(
        "travellers",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("booking_id", sa.String(36), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("identity_reference", sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_travellers_booking_id", "travellers", ["booking_id"])
    op.create_table(
        "tickets",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("booking_id", sa.String(36), nullable=False),
        sa.Column("traveller_id", sa.String(36), nullable=False),
        sa.Column("seat_id", sa.String(36), nullable=True),
        sa.Column("boarding_station_id", sa.String(36), nullable=False),
        sa.Column("arrival_station_id", sa.String(36), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("fare_amount_minor", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["traveller_id"], ["travellers.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(["seat_id"], ["seats.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["boarding_station_id"], ["stations.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["arrival_station_id"], ["stations.id"], ondelete="RESTRICT"
        ),
    )
    for column in ("booking_id", "traveller_id", "seat_id"):
        op.create_index(f"ix_tickets_{column}", "tickets", [column])
    op.create_table(
        "fares",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("booking_id", sa.String(36), nullable=False),
        sa.Column("seat_class", sa.String(30), nullable=False),
        sa.Column("amount_minor", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("booking_id", "seat_class", name="uq_fare_booking_class"),
    )
    op.create_index("ix_fares_booking_id", "fares", ["booking_id"])
    op.create_table(
        "payment_attempts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("booking_id", sa.String(36), nullable=False),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("status", payment_status, nullable=False),
        sa.Column("amount_minor", sa.Integer(), nullable=False),
        sa.Column("provider_reference", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "ix_payment_attempts_booking_id", "payment_attempts", ["booking_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_payment_attempts_booking_id", table_name="payment_attempts")
    op.drop_table("payment_attempts")
    op.drop_index("ix_fares_booking_id", table_name="fares")
    op.drop_table("fares")
    for column in ("seat_id", "traveller_id", "booking_id"):
        op.drop_index(f"ix_tickets_{column}", table_name="tickets")
    op.drop_table("tickets")
    op.drop_index("ix_travellers_booking_id", table_name="travellers")
    op.drop_table("travellers")
    op.drop_index("ix_bookings_service_id", table_name="bookings")
    op.drop_index("ix_bookings_user_id", table_name="bookings")
    op.drop_table("bookings")
    sa.Enum(name="payment_attempt_status_enum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="booking_status_enum").drop(op.get_bind(), checkfirst=True)
