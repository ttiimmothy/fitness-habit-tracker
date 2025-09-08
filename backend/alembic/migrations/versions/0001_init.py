"""init schema

Revision ID: 0001_init
Revises: 
Create Date: 2025-09-07
"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
  op.create_table(
    "users",
    sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
    sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
    sa.Column("password_hash", sa.String(255), nullable=False),
    sa.Column("name", sa.String(255), nullable=True),
    sa.Column("avatar_url", sa.String(512), nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True),server_default=sa.text("now()")),
  )

  op.create_table(
    "habits",
    sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
    sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
    sa.Column("title", sa.String(255), nullable=False),
    sa.Column("frequency", sa.Enum("daily", "weekly", name="frequency"), nullable=False),
    sa.Column("target", sa.Integer(), nullable=False, server_default="1"),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
  )

  op.create_table(
    "habit_logs",
    sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
    sa.Column("habit_id", pg.UUID(as_uuid=True), sa.ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True),
    sa.Column("date", sa.Date(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    sa.UniqueConstraint("habit_id", "date", name="uq_habit_date"),
  )

  op.create_table(
    "badges",
    sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
    sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
    sa.Column("code", sa.String(64), nullable=False, unique=True),
    sa.Column("achieved_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
  )


def downgrade() -> None:
  op.drop_table("badges")
  op.drop_table("habit_logs")
  op.drop_table("habits")
  op.execute("DROP TYPE IF EXISTS frequency")
  op.drop_table("users")
