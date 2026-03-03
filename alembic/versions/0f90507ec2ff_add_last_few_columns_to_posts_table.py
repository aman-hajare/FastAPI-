"""add last few columns to posts table

Revision ID: 0f90507ec2ff
Revises: 005ed9e7c251
Create Date: 2026-02-27 23:02:00.731625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f90507ec2ff'
down_revision: Union[str, Sequence[str], None] = '005ed9e7c251'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts',sa.Column('create_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'create_at')
    pass
