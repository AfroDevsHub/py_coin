"""added profiles_model

Revision ID: 37733f744f98
Revises: 3c6f90022c25
Create Date: 2024-03-26 18:47:07.171822

"""
from enum import Enum
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from lib.utils.constants.users import AccountCountry, AccountLanguage, AccountOccupation, Gender, ProfileInterest

# revision identifiers, used by Alembic.
revision: str = '37733f744f98'
down_revision: Union[str, None] = '3c6f90022c25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'profiles',
        sa.Column(
        "id",
        sa.String(256),
        default=sa.text(f"'{str(uuid4())}'"),
        primary_key=True,
    ),
    sa.Column(
        "profile_id", sa.String(256), default=sa.text(f"'{str(uuid4())}'")
    ),
    sa.Column(
        "account_id", sa.String(256), sa.ForeignKey("accounts.account_id"), nullable=False
    ),
    sa.Column("first_name", sa.String(256), nullable=False),
    sa.Column("last_name", sa.String(256), nullable=False),
    sa.Column("username", sa.String(256), nullable=False),
    sa.Column(
        "date_of_birth", sa.Date, nullable=False
    ),
    sa.Column("gender", sa.Enum(Gender, name='genders_enums'), nullable=False),
    sa.Column("profile_picture", sa.LargeBinary, nullable=False),
    sa.Column("mobile_number", sa.String(256), nullable=False),
    sa.Column(
        "country", sa.Enum(AccountCountry, name='countries_enums'), nullable=False
    ),
    sa.Column(
        "language", sa.Enum(AccountLanguage, name='languages_enums'), default=AccountLanguage.ENGLISH
    ),
    sa.Column(
        "biography", sa.String(256), default="This user has not provided a bio yet."
    ),
    sa.Column(
        "occupation", sa.Enum(AccountOccupation, name='occupations_enums'), default=AccountOccupation.OTHER
    ),
    sa.Column("interests", sa.ARRAY(sa.String(256)), nullable=False),
    sa.Column("social_media_links", sa.JSON, nullable=False),
    sa.Column(
        "created_date", sa.DateTime, default=sa.text("CURRENT_TIMESTAMP")
    ),
    sa.Column(
        "updated_date",
        sa.DateTime,
        default=sa.text("CURRENT_TIMESTAMP"),
        onupdate=sa.text("CURRENT_TIMESTAMP"),
    ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    # ### end Alembic commands ###