"""add_habit_completions_table

Revision ID: 1a885a71679c
Revises: d55da42a0acc
Create Date: 2025-09-17 16:53:09.945855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a885a71679c'
down_revision: Union[str, Sequence[str], None] = 'd55da42a0acc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  # Create habit_completions table
  op.create_table(
      'habit_completions',
      sa.Column('id', sa.UUID(), nullable=False),
      sa.Column('habit_id', sa.UUID(), nullable=False),
      sa.Column('date', sa.Date(), nullable=False),
      sa.Column('is_completed', sa.Boolean(), nullable=False),
      sa.Column('target_at_time', sa.Integer(), nullable=False),
      sa.Column('quantity_achieved', sa.Integer(), nullable=False),
      sa.Column('created_at', sa.DateTime(), nullable=False),
      sa.Column('updated_at', sa.DateTime(), nullable=False),
      sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ondelete='CASCADE'),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('habit_id', 'date',
                          name='uq_habit_completions_habit_date')
  )

  # Create indexes for better query performance
  op.create_index('idx_habit_completions_habit_date',
                  'habit_completions', ['habit_id', 'date'])
  op.create_index('idx_habit_completions_date', 'habit_completions', ['date'])
  op.create_index('idx_habit_completions_completed',
                  'habit_completions', ['is_completed'])


def downgrade() -> None:
  """Downgrade schema."""
  # Drop indexes
  op.drop_index('idx_habit_completions_completed',
                table_name='habit_completions')
  op.drop_index('idx_habit_completions_date', table_name='habit_completions')
  op.drop_index('idx_habit_completions_habit_date',
                table_name='habit_completions')

  # Drop table
  op.drop_table('habit_completions')
