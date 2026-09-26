"""Create seats table with per-coach seat-number uniqueness."""

import sqlalchemy as sa
from alembic import op

revision = "20260927_01"
down_revision = "20260924_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    berth_type = sa.Enum(
        "LOWER",
        "MIDDLE",
        "UPPER",
        "SIDE_LOWER",
        "SIDE_UPPER",
        "SEAT",
        name="berth_type_enum",
    )
    berth_type.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "seats",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("coach_id", sa.String(length=36), nullable=False),
        sa.Column("seat_number", sa.String(length=10), nullable=False),
        sa.Column("berth_type", berth_type, nullable=False),
        sa.ForeignKeyConstraint(["coach_id"], ["coaches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("coach_id", "seat_number", name="uq_seat_coach_number"),
    )
    op.create_index(op.f("ix_seats_coach_id"), "seats", ["coach_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_seats_coach_id"), table_name="seats")
    op.drop_table("seats")
    sa.Enum(name="berth_type_enum").drop(op.get_bind(), checkfirst=True)
