"""create posts table

Revision ID: 28a3b4cf2628
Revises: 
Create Date: 2023-04-21 13:20:17.198418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28a3b4cf2628'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
        )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
