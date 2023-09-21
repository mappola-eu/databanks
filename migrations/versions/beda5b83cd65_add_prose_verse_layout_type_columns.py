"""add prose/verse layout type columns

Revision ID: beda5b83cd65
Revises: 31c48b583e9a
Create Date: 2023-09-21 11:30:06.382600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beda5b83cd65'
down_revision = '31c48b583e9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verse_layout_prose_layout_type_assoc',
    sa.Column('verse_layout_id', sa.Integer(), nullable=True),
    sa.Column('prose_verse_distinction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prose_verse_distinction_id'], ['layout_types.id'], ),
    sa.ForeignKeyConstraint(['verse_layout_id'], ['verse_layouts.id'], )
    )
    op.create_table('verse_layout_verse_layout_type_assoc',
    sa.Column('verse_layout_id', sa.Integer(), nullable=True),
    sa.Column('layout_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['layout_type_id'], ['layout_types.id'], ),
    sa.ForeignKeyConstraint(['verse_layout_id'], ['verse_layouts.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verse_layout_verse_layout_type_assoc')
    op.drop_table('verse_layout_prose_layout_type_assoc')
    # ### end Alembic commands ###
