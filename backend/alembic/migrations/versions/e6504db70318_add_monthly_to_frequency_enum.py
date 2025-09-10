"""add_monthly_to_frequency_enum

Revision ID: e6504db70318
Revises: b657aee89011
Create Date: 2025-09-10 05:23:46.552480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6504db70318'
down_revision: Union[str, Sequence[str], None] = 'b657aee89011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  # Add 'monthly' to the existing frequency enum
  op.execute("ALTER TYPE frequency ADD VALUE 'monthly'")


def downgrade() -> None:
  """Downgrade schema."""
  # Note: PostgreSQL doesn't support removing enum values directly
  # This would require recreating the enum type and updating all references
  # For now, we'll leave the monthly value in place
  pass
