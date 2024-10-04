"""add alarm_history

Revision ID: 70ff4708cdcb
Revises: 07a2be7f77f1
Create Date: 2024-10-04 12:37:39.445677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70ff4708cdcb'
down_revision: Union[str, None] = '07a2be7f77f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alarm_history',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('place_id', sa.BigInteger(), nullable=False),
    sa.Column('alarm_id', sa.BigInteger(), nullable=False),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('dt_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['alarm_id'], ['alarm_messages.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('alarm_history')
    # ### end Alembic commands ###
