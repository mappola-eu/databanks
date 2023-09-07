"""Add verse layouts

Revision ID: 5b9ed241643a
Revises: 070f80b2f4c8
Create Date: 2023-09-07 12:47:36.332886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b9ed241643a'
down_revision = '070f80b2f4c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verse_layouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('prose_verse_presence_id', sa.Integer(), nullable=True),
    sa.Column('scriptio_continua_in_verse_part', sa.Boolean(), nullable=True),
    sa.Column('abbreviations_in_verse_part', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.ForeignKeyConstraint(['prose_verse_presence_id'], ['prose_verse_presences.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('verse_layout_prose_verse_distinction_assoc',
    sa.Column('verse_layout_id', sa.Integer(), nullable=True),
    sa.Column('prose_verse_distinction_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prose_verse_distinction_id'], ['prose_verse_distinctions.id'], ),
    sa.ForeignKeyConstraint(['verse_layout_id'], ['verse_layouts.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verse_layout_prose_verse_distinction_assoc')
    op.drop_table('verse_layouts')
    # ### end Alembic commands ###
