"""Create coaches table."""

import sqlalchemy as sa
from alembic import op

revision = "20260923_02"
down_revision = "20260923_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    seat_class = sa.Enum(
        "FIRST_AC",
        "SECOND_AC",
        "THIRD_AC",
        "SLEEPER",
        "GENERAL",
        name="seat_class_enum",
    )
    seat_class.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "coaches",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("train_id", sa.String(length=36), nullable=False),
        sa.Column("coach_number", sa.String(length=10), nullable=False),
        sa.Column("seat_class", seat_class, nullable=False),
        sa.Column("total_seats", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["train_id"], ["trains.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("train_id", "coach_number", name="uq_coach_train_number"),
    )
    op.create_index(op.f("ix_coaches_train_id"), "coaches", ["train_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_coaches_train_id"), table_name="coaches")
    op.drop_table("coaches")
    sa.Enum(name="seat_class_enum").drop(op.get_bind(), checkfirst=True)
