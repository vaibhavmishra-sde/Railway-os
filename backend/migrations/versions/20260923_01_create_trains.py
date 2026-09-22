"""Create trains table."""

import sqlalchemy as sa
from alembic import op

revision = "20260923_01"
down_revision = "20260922_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "trains",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("number", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("number"),
    )
    op.create_index(op.f("ix_trains_number"), "trains", ["number"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_trains_number"), table_name="trains")
    op.drop_table("trains")
