"""Update created_at column default

Revision ID: 738a789ab2ed
Revises: 7aaab9ce7dff
Create Date: 2024-12-19 20:55:16.313047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '738a789ab2ed'
down_revision: Union[str, None] = '7aaab9ce7dff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update the default value for the created_at column
    op.alter_column(
        'users',
        'created_at',
        server_default=sa.text('NOW()'),
        existing_type=sa.TIMESTAMP(timezone=True),
        existing_nullable=False
    )


def downgrade() -> None:
    # Revert the default value back to now()
    op.alter_column(
        'users',
        'created_at',
        server_default=sa.text('now()'),
        existing_type=sa.TIMESTAMP(timezone=True),
        existing_nullable=False
    )
