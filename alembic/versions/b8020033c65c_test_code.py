"""test code

Revision ID: b8020033c65c
Revises: ff6b9d003fbc
Create Date: 2025-02-22 11:27:09.932847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8020033c65c'
down_revision: Union[str, None] = 'ff6b9d003fbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('code', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test', 'code')
    # ### end Alembic commands ###
