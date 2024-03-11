"""added accounts model

Revision ID: 3c6f90022c25
Revises: d79c0f3b8be1
Create Date: 2024-03-10 19:23:34.472583

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from lib.utils.constants.users import AccountRole, AccountStatus

# revision identifiers, used by Alembic.
revision: str = '3c6f90022c25'
down_revision: Union[str, None] = 'd79c0f3b8be1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_accounts",
        sa.Column("account_id", sa.String(256), nullable=False, unique=True, default=sa.text(f"'{str(uuid4())}'"), primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("account_status", sa.Enum(AccountStatus, name='user_account_statuses'), unique=False, default=AccountStatus.NEW),
        sa.Column("account_email_status", sa.Enum(AccountStatus, name='user_email_account_statuses'), unique=False, default=AccountStatus.UNVERIFIED),
        sa.Column("account_creation_date", sa.DateTime(), default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("account_updated_date", sa.DateTime(), default=sa.text("CURRENT_TIMESTAMP"), onupdate=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("account_status_updated_date", sa.DateTime(), default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("last_login_date", sa.DateTime(), nullable=True),
        sa.Column("account_role", sa.Enum(AccountRole, name='user_account_roles'), nullable=False, default=AccountRole.USER),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_accounts')
    # ### end Alembic commands ###