"""Create dated train services and scheduled stops tables."""

import sqlalchemy as sa
from alembic import op

revision = "20260924_02"
down_revision = "20260924_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    service_status = sa.Enum("SCHEDULED", "RUNNING", "COMPLETED", "CANCELLED", name="service_status_enum")
    service_status.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "train_services",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("train_id", sa.String(length=36), nullable=False),
        sa.Column("route_id", sa.String(length=36), nullable=False),
        sa.Column("service_date", sa.Date(), nullable=False),
        sa.Column("status", service_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["route_id"], ["routes.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["train_id"], ["trains.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("train_id", "service_date", name="uq_service_train_date"),
    )
    op.create_index(op.f("ix_train_services_service_date"), "train_services", ["service_date"], unique=False)
    op.create_index(op.f("ix_train_services_train_id"), "train_services", ["train_id"], unique=False)
    op.create_table(
        "service_stops",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("service_id", sa.String(length=36), nullable=False),
        sa.Column("station_id", sa.String(length=36), nullable=False),
        sa.Column("stop_sequence", sa.Integer(), nullable=False),
        sa.Column("scheduled_arrival", sa.Time(), nullable=True),
        sa.Column("scheduled_departure", sa.Time(), nullable=True),
        sa.Column("platform_number", sa.String(length=10), nullable=True),
        sa.ForeignKeyConstraint(["service_id"], ["train_services.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["station_id"], ["stations.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("service_id", "stop_sequence", name="uq_service_stop_sequence"),
    )
    op.create_index(op.f("ix_service_stops_service_id"), "service_stops", ["service_id"], unique=False)
    op.create_index(op.f("ix_service_stops_station_id"), "service_stops", ["station_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_service_stops_station_id"), table_name="service_stops")
    op.drop_index(op.f("ix_service_stops_service_id"), table_name="service_stops")
    op.drop_table("service_stops")
    op.drop_index(op.f("ix_train_services_train_id"), table_name="train_services")
    op.drop_index(op.f("ix_train_services_service_date"), table_name="train_services")
    op.drop_table("train_services")
    sa.Enum(name="service_status_enum").drop(op.get_bind(), checkfirst=True)
