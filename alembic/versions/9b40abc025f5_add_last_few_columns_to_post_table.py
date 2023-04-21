"""add last few columns to post table

Revision ID: 9b40abc025f5
Revises: d60c4ea312ab
Create Date: 2023-04-21 14:00:01.575103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b40abc025f5'
down_revision = 'd60c4ea312ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts', 
        sa.Column('published', sa.Boolean(), server_default='TRUE')
        )
    op.add_column(
        'posts', 
        sa.Column(
            'created_at', 
            sa.TIMESTAMP(timezone=True), 
            nullable=False, 
            server_default=sa.text('NOW()')
            )
        )
    op.add_column(
        'posts', 
        sa.Column('votes', sa.Integer(), server_default='0', nullable=False)
        )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'votes')
    pass
