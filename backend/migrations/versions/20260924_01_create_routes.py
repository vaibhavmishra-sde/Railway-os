"""Create routes and route stops tables."""

import sqlalchemy as sa
from alembic import op

revision = "20260924_01"
down_revision = "20260923_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "routes",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("total_distance_km", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_routes_code"), "routes", ["code"], unique=False)
    op.create_table(
        "route_stops",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("route_id", sa.String(length=36), nullable=False),
        sa.Column("station_id", sa.String(length=36), nullable=False),
        sa.Column("stop_sequence", sa.Integer(), nullable=False),
        sa.Column("distance_from_origin_km", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["route_id"], ["routes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["station_id"], ["stations.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("route_id", "station_id", name="uq_route_stop_station"),
        sa.UniqueConstraint("route_id", "stop_sequence", name="uq_route_stop_sequence"),
    )
    op.create_index(op.f("ix_route_stops_route_id"), "route_stops", ["route_id"], unique=False)
    op.create_index(op.f("ix_route_stops_station_id"), "route_stops", ["station_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_route_stops_station_id"), table_name="route_stops")
    op.drop_index(op.f("ix_route_stops_route_id"), table_name="route_stops")
    op.drop_table("route_stops")
    op.drop_index(op.f("ix_routes_code"), table_name="routes")
    op.drop_table("routes")
