"""create raw_orders table

Revision ID: 48b76aaa6968
Revises: c363927cd68b
Create Date: 2020-04-02 10:42:06.114463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48b76aaa6968'
down_revision = 'c363927cd68b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'raw_orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pancake_id', sa.BigInteger, nullable=False, unique=True),
        sa.Column('pancake_shop_id', sa.BigInteger, nullable=False),
        sa.Column('payload', sa.JSON, nullable=True),
        sa.Column(
            'inserted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_index(
        'raw_orders_idx_pancake_id',
        'raw_orders',
        ['pancake_id'],
    )

    op.create_index(
        'raw_orders_idx_pancake_shop_id',
        'raw_orders',
        ['pancake_shop_id'],
    )

    op.create_index(
        'raw_orders_idx_inserted_at',
        'raw_orders',
        ['inserted_at'],
        postgresql_ops={'inserted_at': 'DESC'},
    )


def downgrade():
    op.drop_table('raw_orders')
