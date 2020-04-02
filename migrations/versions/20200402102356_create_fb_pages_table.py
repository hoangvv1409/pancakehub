"""create fb_pages table

Revision ID: a14cb100c71c
Revises: 868ed97ab41f
Create Date: 2020-04-02 10:23:56.488474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a14cb100c71c'
down_revision = '868ed97ab41f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'fb_pages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('fb_page_id', sa.BigInteger, nullable=False, unique=True),
        sa.Column('pancake_shop_id', sa.BigInteger, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_index(
        'fb_pages_idx_pancake_shop_id',
        'fb_pages',
        ['pancake_shop_id'],
    )

    op.create_index(
        'fb_pages_idx_fb_page_id',
        'fb_pages',
        ['fb_page_id'],
    )


def downgrade():
    op.drop_table('fb_pages')