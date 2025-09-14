"""add_hobby_to_category_enum

Revision ID: e28666166609
Revises: aefa03a3164b
Create Date: 2025-09-14 02:20:38.779758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e28666166609'
down_revision: Union[str, Sequence[str], None] = 'aefa03a3164b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  # Add 'hobby' to the existing category enum
  op.execute("ALTER TYPE category ADD VALUE 'hobby'")


def downgrade() -> None:
  """Downgrade schema."""
  # Note: PostgreSQL doesn't support removing enum values directly
  # This would require recreating the enum type and updating all references
  # For now, we'll leave the hobby value in the enum
  pass
