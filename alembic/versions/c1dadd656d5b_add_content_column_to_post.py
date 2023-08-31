"""add content column to post

Revision ID: c1dadd656d5b
Revises: d80492f5561f
Create Date: 2023-08-27 13:05:00.699604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1dadd656d5b'
down_revision: Union[str, None] = 'd80492f5561f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
