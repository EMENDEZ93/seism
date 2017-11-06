"""empty message

Revision ID: 67dc23d50022
Revises: cc2b71f2a348
Create Date: 2017-11-06 13:55:13.532394

"""

# revision identifiers, used by Alembic.
revision = '67dc23d50022'
down_revision = 'cc2b71f2a348'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('arduino',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alert_date', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('arduino')
    # ### end Alembic commands ###