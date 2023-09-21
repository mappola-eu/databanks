"""add carmen reading signs assoc

Revision ID: 20dba069c76a
Revises: beda5b83cd65
Create Date: 2023-09-21 11:33:17.961661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20dba069c76a'
down_revision = 'beda5b83cd65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verse_layout_carmen_reading_signs_assoc',
    sa.Column('verse_layout_id', sa.Integer(), nullable=True),
    sa.Column('carmen_reading_sign_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['carmen_reading_sign_id'], ['carmen_reading_signs.id'], ),
    sa.ForeignKeyConstraint(['verse_layout_id'], ['verse_layouts.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verse_layout_carmen_reading_signs_assoc')
    # ### end Alembic commands ###
