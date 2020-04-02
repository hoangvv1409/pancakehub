"""create orders table

Revision ID: c10b1f44ebc5
Revises: 48b76aaa6968
Create Date: 2020-04-02 21:50:26.081548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c10b1f44ebc5'
down_revision = '48b76aaa6968'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pancake_id', sa.BigInteger, nullable=False, unique=True),
        sa.Column('pancake_shop_id', sa.BigInteger, nullable=False),
        sa.Column('fb_page_id', sa.BigInteger, nullable=True),
        sa.Column(
            'inserted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('order_id', sa.String, nullable=True),
        sa.Column('full_name', sa.String, nullable=False),
        sa.Column('phone_number', sa.String, nullable=False),
        sa.Column('full_address', sa.String, nullable=False),
        sa.Column('city', sa.String, nullable=True),
        sa.Column('province_id', sa.Integer, nullable=True),
        sa.Column('district_id', sa.Integer, nullable=True),
        sa.Column('total_cod', sa.Integer, nullable=False),
        sa.Column('status', sa.Integer, nullable=False),
        sa.Column('status_str', sa.String, nullable=True),
        sa.Column('partner_id', sa.Integer, nullable=True),
        sa.Column('partner_str', sa.String, nullable=True),
        sa.Column(
            'status_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sale', sa.String, nullable=True),
        sa.Column('tracking_numbers', sa.String, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_index(
        'orders_idx_pancake_id',
        'orders',
        ['pancake_id'],
    )

    op.create_index(
        'orders_idx_pancake_shop_id',
        'orders',
        ['pancake_shop_id'],
    )


def downgrade():
    op.drop_table('orders')
