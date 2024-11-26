"""Add classrooms table

Revision ID: b1541ff3db16
Revises: 681641d9c945
Create Date: 2024-11-26 17:57:13.515666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1541ff3db16'
down_revision: Union[str, None] = '681641d9c945'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classrooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('short_name', sa.String(length=50), nullable=False),
    sa.Column('building_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classrooms_id'), 'classrooms', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_classrooms_id'), table_name='classrooms')
    op.drop_table('classrooms')
    # ### end Alembic commands ###
