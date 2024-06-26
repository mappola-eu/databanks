"""Add epidoc converted cache columns

Revision ID: 83ff8e9b310a
Revises: f9ece37b01d7
Create Date: 2022-11-02 14:03:40.586014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83ff8e9b310a'
down_revision = 'f9ece37b01d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inscriptions', sa.Column('text_interpretative_cached', sa.Text(), nullable=True))
    op.add_column('inscriptions', sa.Column('text_diplomatic_cached', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inscriptions', 'text_diplomatic_cached')
    op.drop_column('inscriptions', 'text_interpretative_cached')
    # ### end Alembic commands ###
