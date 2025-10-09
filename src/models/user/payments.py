"""Payments: Payments Profile Model."""

from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, Enum, Float, ForeignKey, String, text
from src.lib.utils.constants.users import Status
from src.models import Base


class PaymentProfile(Base):
    """Model representing a User's Payment Information."""

    __tablename__ = "payment_profiles"
    __table_args__ = ({"schema": "users"},)

    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        nullable=False,
        primary_key=True,
    )
    payment_id = Column("payment_id", UUID(as_uuid=True), nullable=False, default=uuid4, unique=True)
    account_id = Column(
        "account_id",
        UUID(as_uuid=True),
        ForeignKey("users.accounts.id"),
        nullable=False,
        unique=True,
    )
    card_id = Column(
        "card_id",
        UUID(as_uuid=True),
        ForeignKey("warehouse.cards.id"),
        nullable=False,
        unique=True,
    )
    name = Column("name", String(256), nullable=False, default="New Payment Account.")
    description = Column(
        "description",
        String(256),
        nullable=False,
        default="New Payment Account Created for Block Chain Transactions.",
    )
    status: Status | Column[Status] = Column(
        "status", Enum(Status, name="card_status"), default=Status.NEW, nullable=False
    )
    balance: float | Column[float] = Column(
        "balance", Float, default=0.0, nullable=False
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

    def __str__(self) -> str:
        """String Representation of the Payment Profile Object."""

        return f"Payment ID: {str(self.payment_id)}, Account ID: {self.account_id}, Status: {self.status}, Balance: {self.balance}"

    def __repr__(self) -> str:
        """Recreates an Object: Representation of the Payment Profile Object."""

        return f"PaymentProfile({self.payment_id}, {self.account_id}, {self.status}, {self.balance})"
