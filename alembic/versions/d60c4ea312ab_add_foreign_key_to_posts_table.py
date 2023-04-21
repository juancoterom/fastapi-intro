"""add foreign-key to posts table

Revision ID: d60c4ea312ab
Revises: e65dc49fc583
Create Date: 2023-04-21 13:54:49.474799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd60c4ea312ab'
down_revision = 'e65dc49fc583'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False),
        )
    op.create_foreign_key(
        'post_users_fk', 
        source_table='posts', 
        referent_table='users', 
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete='CASCADE'
        )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
