"""add content column to post table

Revision ID: 51873f6355ab
Revises: 5de2b6399b22
Create Date: 2021-12-30 15:44:41.211144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51873f6355ab'
down_revision = '5de2b6399b22'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
