"""Add publication order number

Revision ID: 36d35faa315c
Revises: b5de036bf0ed
Create Date: 2022-12-21 22:14:45.610470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36d35faa315c'
down_revision = 'b5de036bf0ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('publications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_number', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('publications', schema=None) as batch_op:
        batch_op.drop_column('order_number')

    # ### end Alembic commands ###
