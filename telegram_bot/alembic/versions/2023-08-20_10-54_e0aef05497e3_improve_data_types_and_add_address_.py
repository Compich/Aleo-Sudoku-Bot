"""Improve data types and add address privacy field

Revision ID: e0aef05497e3
Revises: 28bdd77685af
Create Date: 2023-08-20 10:54:31.634709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0aef05497e3'
down_revision: Union[str, None] = '28bdd77685af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('address_privacy', sa.Enum('PUBLIC', 'HIDDEN', 'PRIVATE', name='address_privacy'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'address_privacy')
    # ### end Alembic commands ###
