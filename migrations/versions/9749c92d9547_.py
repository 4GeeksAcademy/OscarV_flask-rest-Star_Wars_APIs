"""empty message

Revision ID: 9749c92d9547
Revises: 051267cf4361
Create Date: 2025-02-26 23:24:15.636858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9749c92d9547'
down_revision = '051267cf4361'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('rotation_period', sa.Integer(), nullable=False),
    sa.Column('orbital_period', sa.Integer(), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=False),
    sa.Column('climate', sa.String(length=250), nullable=False),
    sa.Column('terrain', sa.String(length=250), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('planets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('rotation_period', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('orbital_period', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('diameter', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('climate', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('terrain', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('population', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='planets_pkey')
    )
    op.drop_table('planet')
    # ### end Alembic commands ###
