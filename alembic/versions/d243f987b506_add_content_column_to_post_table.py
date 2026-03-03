"""add content column to post table

Revision ID: d243f987b506
Revises: 8d4e03cd615e
Create Date: 2026-02-27 22:13:34.697437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd243f987b506'
down_revision: Union[str, Sequence[str], None] = '8d4e03cd615e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
