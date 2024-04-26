"""removed nullable requirement for testing

Revision ID: d72b97068700
Revises: 37c7bc35ca63
Create Date: 2024-04-25 18:36:24.631951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72b97068700'
down_revision = '37c7bc35ca63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('score',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('lives',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('difficulty_level',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('answer',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('num_min',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('num_max',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('num_max',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('num_min',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('answer',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('difficulty_level',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('lives',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.alter_column('score',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
