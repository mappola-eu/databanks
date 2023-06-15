"""Add images class

Revision ID: ea96b23fb8b9
Revises: 9db091944c02
Create Date: 2023-06-15 10:54:05.695754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea96b23fb8b9'
down_revision = '9db091944c02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('image_link', sa.Text(), nullable=True),
    sa.Column('image_alt', sa.Text(), nullable=True),
    sa.Column('image_citation', sa.String(length=210), nullable=True),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
