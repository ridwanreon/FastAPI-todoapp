"""phone number adding for our users table

Revision ID: 3fccdd82f57c
Revises: 
Create Date: 2026-08-10 23:17:26.141329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fccdd82f57c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Users',sa.Column('Phone_number',sa.String(20),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
