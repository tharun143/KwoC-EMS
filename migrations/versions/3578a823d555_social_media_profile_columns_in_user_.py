"""social media profile columns in user model

Revision ID: 3578a823d555
Revises: 74be57a2d202
Create Date: 2020-05-12 02:30:18.631348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3578a823d555'
down_revision = '74be57a2d202'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('facebook', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('linkedin', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('twitter', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'twitter')
    op.drop_column('user', 'linkedin')
    op.drop_column('user', 'facebook')
    # ### end Alembic commands ###
