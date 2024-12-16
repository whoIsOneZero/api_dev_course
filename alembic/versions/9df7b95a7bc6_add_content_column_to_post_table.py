"""add content column to post table

Revision ID: 9df7b95a7bc6
Revises: 86c135c92cc9
Create Date: 2024-12-16 15:47:33.544404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9df7b95a7bc6'
down_revision: Union[str, None] = '86c135c92cc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
