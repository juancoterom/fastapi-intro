"""add content column to posts table

Revision ID: b2d13d3faf31
Revises: 28a3b4cf2628
Create Date: 2023-04-21 13:39:49.822778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2d13d3faf31'
down_revision = '28a3b4cf2628'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
        )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
