"""add_provider_field_to_user

Revision ID: 5d6a5c918d3e
Revises: e28666166609
Create Date: 2025-09-14 08:29:34.430185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d6a5c918d3e'
down_revision: Union[str, Sequence[str], None] = 'e28666166609'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  # Create the provider enum type
  provider_enum = sa.Enum('email', 'google', name='provider')
  provider_enum.create(op.get_bind())

  # Add the provider column to users table
  op.add_column('users', sa.Column('provider', provider_enum, nullable=True))


def downgrade() -> None:
  """Downgrade schema."""
  # Remove the provider column
  op.drop_column('users', 'provider')

  # Drop the provider enum type
  sa.Enum(name='provider').drop(op.get_bind())
