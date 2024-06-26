"""Add more ORM data - now more relations (II)

Revision ID: a9843ae44402
Revises: 6e836e3d62c2
Create Date: 2021-04-06 14:37:14.258362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9843ae44402'
down_revision = '6e836e3d62c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inscription_dating_criterion_assoc',
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('dating_criterion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dating_criterion_id'], ['dating_criteria.id'], ),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], )
    )
    op.create_table('inscription_decoration_tag_assoc',
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('object_decoration_tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.ForeignKeyConstraint(['object_decoration_tag_id'], ['object_decoration_tags.id'], )
    )
    op.create_table('inscription_language_assoc',
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['languages.id'], )
    )
    op.create_table('inscription_verse_type_assoc',
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('verse_type_id', sa.Integer(), nullable=True),
    sa.Column('verse_timing_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.ForeignKeyConstraint(['verse_timing_type_id'], ['verse_timing_types.id'], ),
    sa.ForeignKeyConstraint(['verse_type_id'], ['verse_types.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inscription_verse_type_assoc')
    op.drop_table('inscription_language_assoc')
    op.drop_table('inscription_decoration_tag_assoc')
    op.drop_table('inscription_dating_criterion_assoc')
    # ### end Alembic commands ###
