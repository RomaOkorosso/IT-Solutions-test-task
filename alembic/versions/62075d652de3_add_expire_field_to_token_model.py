"""add expire field to token model

Revision ID: 62075d652de3
Revises: a79dc7c99970
Create Date: 2024-06-07 23:47:02.297339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "62075d652de3"
down_revision: Union[str, None] = "a79dc7c99970"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tokens", sa.Column("expire_at", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tokens", "expire_at")
    # ### end Alembic commands ###