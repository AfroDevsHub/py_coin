"""init migration

Revision ID: d79c0f3b8be1
Revises: 
Create Date: 2024-03-06 23:30:51.752142

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d79c0f3b8be1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id", sa.String(256), default=f"'{str(uuid4())}'", nullable=False
        ),
        sa.Column(
            "user_id",
            sa.String(256),
            default=f"'{str(uuid4())}'",
            nullable=False,
        ),
        sa.Column(
            "created", sa.DateTime(), default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.Column("email", sa.String(256), nullable=False, unique=True),
        sa.Column("password", sa.String(256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
