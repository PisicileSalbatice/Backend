"""Add classrooms table

Revision ID: 3312a30ce7d9
Revises: b1541ff3db16
Create Date: 2024-11-26 18:07:38.942286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3312a30ce7d9'
down_revision: Union[str, None] = 'b1541ff3db16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###