"""Add MV cache

Revision ID: 4d2c27ec9d2d
Revises: 83ff8e9b310a
Create Date: 2022-11-10 11:37:48.099414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d2c27ec9d2d'
down_revision = '83ff8e9b310a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inscriptions', sa.Column('text_metrics_visualised_cached', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inscriptions', 'text_metrics_visualised_cached')
    # ### end Alembic commands ###
