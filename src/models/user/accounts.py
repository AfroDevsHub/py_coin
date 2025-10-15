"""Accounts: Accounts Model."""

from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.lib.utils.constants.users import Status
from src.models.user.payments import PaymentProfile
from src.models.user.profiles import UserProfile
from src.models.user.settings import SettingsProfile
from src.models import Base


class Account(Base):
    """Model representing a User's Account."""

    __tablename__ = "accounts"
    __table_args__ = ({"schema": "users"},)

    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        nullable=False,
        primary_key=True,
    )
    account_id = Column(
        "account_id",
        UUID(as_uuid=True),
        default=uuid4,
        unique=True,
    )
    user_id = Column(
        "user_id", UUID(as_uuid=True), ForeignKey("users.users.id"), nullable=False
    )
    status: Status | Column[Status] = Column(
        "status",
        Enum(Status, name="account_status"),
        default=Status.NEW,
        nullable=False,
    )
    created_date = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_date = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    user_profiles = relationship(
        UserProfile, backref="Account", cascade="all, delete-orphan", uselist=False
    )
    payment_profiles = relationship(
        PaymentProfile, backref="Account", cascade="all, delete-orphan", uselist=False
    )
    settings_profile = relationship(
        SettingsProfile, backref="Account", cascade="all, delete-orphan", uselist=False
    )

    def __str__(self) -> str:
        """String Representation of the Account Object."""

        return f"Account ID: {str(self.account_id)}, User ID: {self.user_id}, Status: {self.status}"

    def __repr__(self) -> str:
        """Recreates an Object: Representation of the Account Object."""

        return f"Account({self.account_id}, {self.user_id}, {self.status})"
