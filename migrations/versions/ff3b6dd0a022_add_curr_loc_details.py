"""Add curr. loc details

Revision ID: ff3b6dd0a022
Revises: 9055d852a11d
Create Date: 2022-12-08 23:25:19.222314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff3b6dd0a022'
down_revision = '9055d852a11d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inscriptions', sa.Column('current_location_inventory', sa.String(length=80), nullable=True))
    op.add_column('inscriptions', sa.Column('current_location_details', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inscriptions', 'current_location_details')
    op.drop_column('inscriptions', 'current_location_inventory')
    # ### end Alembic commands ###
