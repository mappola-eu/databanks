"""Add text layout tags

Revision ID: eb90c6dea7b3
Revises: a38d9b920470
Create Date: 2022-12-01 21:23:39.299110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb90c6dea7b3'
down_revision = 'a38d9b920470'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text_layout_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('enum_lod', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inscription_text_layout_tag_assoc',
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('text_layout_tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.ForeignKeyConstraint(['text_layout_tag_id'], ['verse_types.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inscription_text_layout_tag_assoc')
    op.drop_table('text_layout_tags')
    # ### end Alembic commands ###
