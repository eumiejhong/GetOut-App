"""empty message

Revision ID: 8cabb21954a5
Revises: 
Create Date: 2021-06-28 21:25:27.871224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cabb21954a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recreation_gov_sites',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('rec_gov_id', sa.Text(), nullable=True),
    sa.Column('type', sa.Text(), nullable=True),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('directions', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=True),
    sa.Column('state', sa.Text(), nullable=True),
    sa.Column('latitude', sa.Integer(), nullable=True),
    sa.Column('longitude', sa.Integer(), nullable=True),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.Text(), nullable=False),
    sa.Column('last_name', sa.Text(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('city', sa.Text(), nullable=True),
    sa.Column('state', sa.Text(), nullable=True),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('latitude', sa.Integer(), nullable=True),
    sa.Column('longitude', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('liked_sites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rec_gov_id', sa.Text(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['rec_gov_id'], ['recreation_gov_sites.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('liked_site_id', sa.Integer(), nullable=True),
    sa.Column('rec_gov_id', sa.Text(), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('type', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['liked_site_id'], ['liked_sites.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['rec_gov_id'], ['recreation_gov_sites.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('story_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('story_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('story_comments')
    op.drop_table('stories')
    op.drop_table('liked_sites')
    op.drop_table('users')
    op.drop_table('recreation_gov_sites')
    # ### end Alembic commands ###