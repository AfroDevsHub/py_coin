"""added cards warehouse model

Revision ID: 86a881d7f966
Revises: 14e2bd506750
Create Date: 2024-04-02 02:32:46.429097

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from src.lib.utils.constants.users import Status, CardType

# revision identifiers, used by Alembic.
revision: str = "86a881d7f966"
down_revision: Union[str, None] = "14e2bd506750"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS warehouse")
    op.create_table(
        "cards",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            default=sa.text(f"'{str(uuid4())}'"),
            unique=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column(
            "card_id",
            sa.String(256),
            default=sa.text(f"'{str(uuid4())}'"),
            nullable=False,
        ),
        sa.Column("card_number", sa.String(256), nullable=False),
        sa.Column("cvv_number", sa.String(256), nullable=False),
        sa.Column("card_type", sa.Enum(CardType, name="card_type"), nullable=False),
        sa.Column(
            "status",
            sa.Enum(Status, name="card_status"),
            nullable=False,
            default=Status.NEW,
        ),
        sa.Column("pin", sa.String(256), nullable=False),
        sa.Column("expiration_date", sa.Date, nullable=False),
        sa.Column("created_date", sa.DateTime, default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_date",
            sa.DateTime,
            default=sa.text("CURRENT_TIMESTAMP"),
            onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("salt_value", sa.String(256), nullable=False),
        schema="warehouse",
    )


def downgrade() -> None:
    op.drop_table("cards", schema="warehouse")
    op.execute("DROP TYPE IF EXISTS card_type CASCADE")
    op.execute("DROP TYPE IF EXISTS card_status CASCADE")
    op.execute("DROP SCHEMA IF EXISTS warehouse")
