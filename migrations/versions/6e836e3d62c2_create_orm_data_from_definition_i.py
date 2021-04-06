"""create orm data from definition (I)

Revision ID: 6e836e3d62c2
Revises: 
Create Date: 2021-04-06 14:27:39.270678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e836e3d62c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('current_locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dating_criteria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('object_decoration_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('object_execution_techniques',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('object_materials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('object_preservation_states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('object_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_age_expressions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_age_precision',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_ages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_genders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_legal_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_origins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_professions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_ranks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provinces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('text_functions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('verse_timing_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('verse_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('parent_verse_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_verse_type_id'], ['verse_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=180), nullable=True),
    sa.Column('trismegistos_nr', sa.String(length=40), nullable=True),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('find_comment', sa.Text(), nullable=True),
    sa.Column('current_location_id', sa.Integer(), nullable=True),
    sa.Column('object_type_id', sa.Integer(), nullable=True),
    sa.Column('object_material_id', sa.Integer(), nullable=True),
    sa.Column('object_preservation_state_id', sa.Integer(), nullable=True),
    sa.Column('object_execution_technique_id', sa.Integer(), nullable=True),
    sa.Column('object_decoration_comment', sa.Text(), nullable=True),
    sa.Column('object_text_layout_comment', sa.Text(), nullable=True),
    sa.Column('text_function_id', sa.Integer(), nullable=True),
    sa.Column('text_diplomatic_form', sa.Text(), nullable=True),
    sa.Column('text_interpretative_form', sa.Text(), nullable=True),
    sa.Column('text_metrics_visualised_form', sa.Text(), nullable=True),
    sa.Column('text_apparatus_criticus_comment', sa.Text(), nullable=True),
    sa.Column('general_comment', sa.Text(), nullable=True),
    sa.Column('date', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['current_location_id'], ['current_locations.id'], ),
    sa.ForeignKeyConstraint(['object_execution_technique_id'], ['object_execution_techniques.id'], ),
    sa.ForeignKeyConstraint(['object_material_id'], ['object_materials.id'], ),
    sa.ForeignKeyConstraint(['object_preservation_state_id'], ['object_preservation_states.id'], ),
    sa.ForeignKeyConstraint(['object_type_id'], ['object_types.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.ForeignKeyConstraint(['text_function_id'], ['text_functions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reference_link', sa.Text(), nullable=True),
    sa.Column('people_gender_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_gender_id'], ['people_genders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('reference_comment', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('translations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inscription_id', sa.Integer(), nullable=True),
    sa.Column('translated_form', sa.Text(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.Column('link_to_published_transition', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['inscription_id'], ['inscriptions.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['languages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('translations')
    op.drop_table('publications')
    op.drop_table('people')
    op.drop_table('inscriptions')
    op.drop_table('verse_types')
    op.drop_table('verse_timing_types')
    op.drop_table('text_functions')
    op.drop_table('provinces')
    op.drop_table('places')
    op.drop_table('people_ranks')
    op.drop_table('people_professions')
    op.drop_table('people_origins')
    op.drop_table('people_legal_status')
    op.drop_table('people_genders')
    op.drop_table('people_ages')
    op.drop_table('people_age_precision')
    op.drop_table('people_age_expressions')
    op.drop_table('object_types')
    op.drop_table('object_preservation_states')
    op.drop_table('object_materials')
    op.drop_table('object_execution_techniques')
    op.drop_table('object_decoration_tags')
    op.drop_table('languages')
    op.drop_table('dating_criteria')
    op.drop_table('current_locations')
    # ### end Alembic commands ###
