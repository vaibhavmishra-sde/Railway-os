"""Create stations table.

Revision ID: 20260922_01
Revises:
Create Date: 2026-09-22
"""

from alembic import op
import sqlalchemy as sa


revision = "20260922_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the first persisted RailwayOS domain table."""
    op.create_table(
        "stations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("timezone", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_stations_code"), "stations", ["code"], unique=False)


def downgrade() -> None:
    """Remove the stations table."""
    op.drop_index(op.f("ix_stations_code"), table_name="stations")
    op.drop_table("stations")
