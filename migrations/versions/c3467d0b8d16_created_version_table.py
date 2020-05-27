"""Created version table

Revision ID: c3467d0b8d16
Revises: 268ca56106f1
Create Date: 2020-05-26 19:21:16.735026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3467d0b8d16'
down_revision = '268ca56106f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('version',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=True),
    sa.Column('upload_date', sa.DateTime(), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['document_id'], ['document.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('version')
    # ### end Alembic commands ###
