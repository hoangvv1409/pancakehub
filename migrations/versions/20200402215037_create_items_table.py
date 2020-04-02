"""create items table

Revision ID: 9b0b9ec79c36
Revises: c10b1f44ebc5
Create Date: 2020-04-02 21:50:37.307301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b0b9ec79c36'
down_revision = 'c10b1f44ebc5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pancake_id', sa.BigInteger, nullable=False, unique=True),
        sa.Column('pancake_order_id', sa.BigInteger, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('variant', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_index(
        'items_idx_pancake_order_id',
        'items',
        ['pancake_order_id'],
    )


def downgrade():
    op.drop_table('items')
