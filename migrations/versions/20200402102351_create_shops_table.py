"""create shops table

Revision ID: 868ed97ab41f
Revises: 
Create Date: 2020-04-02 10:23:51.631973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '868ed97ab41f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'shops',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pancake_id', sa.BigInteger, nullable=False, unique=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('info', sa.JSON, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )

    op.create_index(
        'shops_idx_pancake_id',
        'shops',
        ['pancake_id'],
    )


def downgrade():
    op.drop_table('shops')
