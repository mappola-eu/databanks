"""Use verse timing type

Revision ID: eba8717adf67
Revises: 6c39d06d66fe
Create Date: 2023-02-16 10:16:06.893869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eba8717adf67'
down_revision = '6c39d06d66fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inscriptions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verse_timing_type_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('verse_timing_type_on_inscription', 'verse_timing_types', ['verse_timing_type_id'], ['id'])

    with op.batch_alter_table('verse_timing_types', schema=None) as batch_op:
        batch_op.drop_column('enum_lod')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('verse_timing_types', schema=None) as batch_op:
        batch_op.add_column(sa.Column('enum_lod', sa.VARCHAR(length=150), nullable=True))

    with op.batch_alter_table('inscriptions', schema=None) as batch_op:
        batch_op.drop_constraint('verse_timing_type_on_inscription', type_='foreignkey')
        batch_op.drop_column('verse_timing_type_id')

    # ### end Alembic commands ###
