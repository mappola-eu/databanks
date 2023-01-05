"""auto-migrations

Revision ID: b5de036bf0ed
Revises: 2f9dea96010f
Create Date: 2022-12-21 22:13:38.957595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5de036bf0ed'
down_revision = '2f9dea96010f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inscriptions', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.TEXT(length=180),
               type_=sa.String(length=180),
               existing_nullable=True)
        batch_op.alter_column('trismegistos_nr',
               existing_type=sa.TEXT(length=40),
               type_=sa.String(length=40),
               existing_nullable=True)

    with op.batch_alter_table('object_decoration_tags', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.TEXT(length=100),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('enum_lod',
               existing_type=sa.TEXT(length=150),
               type_=sa.String(length=150),
               existing_nullable=True)

    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.TEXT(length=100),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.alter_column('ancient_name',
               existing_type=sa.TEXT(length=90),
               type_=sa.String(length=90),
               existing_nullable=True)
        batch_op.alter_column('modern_name',
               existing_type=sa.TEXT(length=90),
               type_=sa.String(length=90),
               existing_nullable=True)
        batch_op.alter_column('enum_lod',
               existing_type=sa.TEXT(length=150),
               type_=sa.String(length=150),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.alter_column('enum_lod',
               existing_type=sa.String(length=150),
               type_=sa.TEXT(length=150),
               existing_nullable=True)
        batch_op.alter_column('modern_name',
               existing_type=sa.String(length=90),
               type_=sa.TEXT(length=90),
               existing_nullable=True)
        batch_op.alter_column('ancient_name',
               existing_type=sa.String(length=90),
               type_=sa.TEXT(length=90),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(length=100),
               type_=sa.TEXT(length=100),
               existing_nullable=True)

    with op.batch_alter_table('object_decoration_tags', schema=None) as batch_op:
        batch_op.alter_column('enum_lod',
               existing_type=sa.String(length=150),
               type_=sa.TEXT(length=150),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(length=100),
               type_=sa.TEXT(length=100),
               existing_nullable=True)

    with op.batch_alter_table('inscriptions', schema=None) as batch_op:
        batch_op.alter_column('trismegistos_nr',
               existing_type=sa.String(length=40),
               type_=sa.TEXT(length=40),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(length=180),
               type_=sa.TEXT(length=180),
               existing_nullable=True)

    # ### end Alembic commands ###