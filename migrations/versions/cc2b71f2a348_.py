"""empty message

Revision ID: cc2b71f2a348
Revises: e487fa33197e
Create Date: 2017-10-26 22:21:24.304090

"""

# revision identifiers, used by Alembic.
revision = 'cc2b71f2a348'
down_revision = 'e487fa33197e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seism', sa.Column('seismic_time', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seism', 'seismic_time')
    # ### end Alembic commands ###