"""Baseline

Revision ID: 28bdd77685af
Revises: 
Create Date: 2023-08-20 02:26:13.564106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28bdd77685af'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('reg_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('view_key', sa.String(length=100), nullable=True),
    sa.Column('private_key', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('games',
    sa.Column('game_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('difficulty', sa.Enum('EASY', 'MEDIUM', 'HARD', 'EXTREME', name='sudoku_difficulty'), nullable=False),
    sa.Column('board_str', sa.String(length=81), nullable=False),
    sa.Column('start_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('game_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('games')
    op.drop_table('users')
    # ### end Alembic commands ###