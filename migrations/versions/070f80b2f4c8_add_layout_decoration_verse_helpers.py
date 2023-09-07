"""add layout/decoration verse helpers

Revision ID: 070f80b2f4c8
Revises: 6e69149a3e62
Create Date: 2023-09-07 12:41:15.107054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '070f80b2f4c8'
down_revision = '6e69149a3e62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carmen_reading_signs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('layout_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prose_verse_distinctions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prose_verse_presences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('verse_line_correspondences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verse_line_correspondences')
    op.drop_table('prose_verse_presences')
    op.drop_table('prose_verse_distinctions')
    op.drop_table('layout_types')
    op.drop_table('carmen_reading_signs')
    # ### end Alembic commands ###
