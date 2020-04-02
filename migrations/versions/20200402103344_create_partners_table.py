"""create partners table

Revision ID: c363927cd68b
Revises: a14cb100c71c
Create Date: 2020-04-02 10:33:44.185442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c363927cd68b'
down_revision = 'a14cb100c71c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'partners',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pancake_id', sa.Integer, nullable=False, unique=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
    )


def downgrade():
    op.drop_table('partners')
