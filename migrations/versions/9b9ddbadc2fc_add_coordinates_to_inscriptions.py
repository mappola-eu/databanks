"""Add coordinates to Inscriptions

Revision ID: 9b9ddbadc2fc
Revises: 36d35faa315c
Create Date: 2022-12-22 10:40:28.409187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b9ddbadc2fc'
down_revision = '36d35faa315c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inscriptions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coordinates_long', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('coordinates_lat', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inscriptions', schema=None) as batch_op:
        batch_op.drop_column('coordinates_lat')
        batch_op.drop_column('coordinates_long')

    # ### end Alembic commands ###
