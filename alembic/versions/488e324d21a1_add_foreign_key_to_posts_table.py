"""add foreign key to posts table

Revision ID: 488e324d21a1
Revises: e75462fb85af
Create Date: 2021-12-30 15:58:13.625353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '488e324d21a1'
down_revision = 'e75462fb85af'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_fk', source_table="posts", referent_table="users", 
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
