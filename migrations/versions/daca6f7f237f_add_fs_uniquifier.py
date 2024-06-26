"""Add fs_uniquifier

Revision ID: daca6f7f237f
Revises: d35fb4428085
Create Date: 2024-05-16 14:19:32.444286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daca6f7f237f'
down_revision = 'd35fb4428085'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fs_uniquifier', sa.String(length=64), nullable=True))
        batch_op.create_unique_constraint('fs_uniquifier_constraint', ['fs_uniquifier'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fs_uniquifier_constraint', type_='unique')
        batch_op.drop_column('fs_uniquifier')

    # ### end Alembic commands ###
