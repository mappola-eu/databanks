"""Add work status / update columns

Revision ID: f9ece37b01d7
Revises: 08db0aa26666
Create Date: 2022-10-13 10:43:00.545939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ece37b01d7'
down_revision = '08db0aa26666'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('work_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('inscriptions', sa.Column('last_updated_at', sa.DateTime(), nullable=True))
    op.add_column('inscriptions', sa.Column('last_updated_by_id', sa.Integer(), nullable=True))
    op.add_column('inscriptions', sa.Column('work_status_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'inscriptions', 'work_status', ['work_status_id'], ['id'])
    op.create_foreign_key(None, 'inscriptions', 'user', ['last_updated_by_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'inscriptions', type_='foreignkey')
    op.drop_constraint(None, 'inscriptions', type_='foreignkey')
    op.drop_column('inscriptions', 'work_status_id')
    op.drop_column('inscriptions', 'last_updated_by_id')
    op.drop_column('inscriptions', 'last_updated_at')
    op.drop_table('work_status')
    # ### end Alembic commands ###
