"""add foreign-key to post table

Revision ID: 005ed9e7c251
Revises: de85c5f41f66
Create Date: 2026-02-27 22:48:51.651182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005ed9e7c251'
down_revision: Union[str, Sequence[str], None] = 'de85c5f41f66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users",local_cols=['owner_id'], 
                          remote_cols=['id'] ,ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
