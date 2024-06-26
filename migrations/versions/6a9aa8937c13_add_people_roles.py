"""add people roles

Revision ID: 6a9aa8937c13
Revises: 5ed7b21772ed
Create Date: 2023-05-04 10:25:02.911274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a9aa8937c13'
down_revision = '5ed7b21772ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('people_role_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key("people_have_roles", 'people_roles', ['people_role_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_constraint("people_have_roles", type_='foreignkey')
        batch_op.drop_column('people_role_id')

    op.drop_table('people_roles')
    # ### end Alembic commands ###
