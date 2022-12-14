"""empty message

Revision ID: 550f6986c6da
Revises: 92e15f67228b
Create Date: 2022-11-11 13:03:12.690027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '550f6986c6da'
down_revision = '92e15f67228b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'query_config', ['parameter'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'query_config', type_='unique')
    # ### end Alembic commands ###
