"""empty message

Revision ID: 0413daa851fe
Revises: 08e6bf983bec
Create Date: 2020-05-05 11:52:10.071404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0413daa851fe'
down_revision = '08e6bf983bec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres_artists',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['Genre.id'], ),
    sa.PrimaryKeyConstraint('genre_id', 'artist_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genres_artists')
    # ### end Alembic commands ###
