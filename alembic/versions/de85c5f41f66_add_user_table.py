"""add user table

Revision ID: de85c5f41f66
Revises: d243f987b506
Create Date: 2026-02-27 22:29:04.489794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de85c5f41f66'
down_revision: Union[str, Sequence[str], None] = 'd243f987b506'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer,nullable=False),
                    sa.Column('email',sa.String,nullable=False),
                    sa.Column('password',sa.String,nullable=False),
                    sa.Column('create_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')          
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
