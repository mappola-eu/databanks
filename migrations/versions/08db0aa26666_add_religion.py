"""Add religion

Revision ID: 08db0aa26666
Revises: 268323578818
Create Date: 2022-10-12 19:04:57.939543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08db0aa26666'
down_revision = '268323578818'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('religions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('inscriptions', sa.Column('religion_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'inscriptions', 'religions', ['religion_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'inscriptions', type_='foreignkey')
    op.drop_column('inscriptions', 'religion_id')
    op.drop_table('religions')
    # ### end Alembic commands ###
