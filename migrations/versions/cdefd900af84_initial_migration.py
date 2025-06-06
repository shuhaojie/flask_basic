"""Initial migration

Revision ID: cdefd900af84
Revises: b2de5f6654bc
Create Date: 2025-06-05 17:31:54.734051

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cdefd900af84'
down_revision = 'b2de5f6654bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(collation='utf8mb4_general_ci', length=120),
               type_=sa.String(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=256),
               type_=mysql.VARCHAR(collation='utf8mb4_general_ci', length=120),
               existing_nullable=False)

    # ### end Alembic commands ###
