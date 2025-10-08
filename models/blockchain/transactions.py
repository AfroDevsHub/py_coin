"""Transactions: Transaction Model."""

from datetime import datetime
from uuid import uuid4, UUID as uuid

from sqlalchemy import UUID, Column, DateTime, Enum, Float, ForeignKey, String, text

from lib.utils.constants.transactions import TransactionStatus
from models import Base


class Transaction(Base):
    """Model representing a Transaction."""

    __tablename__ = "transactions"
    __table_args__ = ({"schema": "blockchain"},)

    id: uuid | Column[uuid] = Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False
    )
    transaction_id: uuid | Column[uuid] = Column(
        "transaction_id", UUID(as_uuid=True), nullable=False
    )
    sender: uuid | Column[uuid] = Column(
        "sender",
        UUID(as_uuid=True),
        ForeignKey("users.payment_profiles.id"),
        nullable=False,
    )
    receiver: uuid | Column[uuid] = Column(
        "receiver",
        UUID(as_uuid=True),
        ForeignKey("users.payment_profiles.id"),
        nullable=False,
    )
    amount: float | Column[float] = Column("amount", Float, nullable=False)
    title: str | Column[str] = Column("title", String(256), nullable=True)
    description: str | Column[str] = Column("description", String(256), nullable=True)
    sender_signiture: str | Column[str] = Column(
        "sender_signiture", String(256), nullable=True
    )
    receiver_signiture: str | Column[str] = Column(
        "receiver_signiture", String(256), nullable=True
    )
    transaction_status: TransactionStatus | Column[TransactionStatus] = Column(
        "transaction_status",
        Enum(TransactionStatus, name="transaction_status"),
        nullable=False,
        default=TransactionStatus.DRAFT,
    )
    salt_value: uuid | Column[uuid] = Column(
        "salt_value", UUID(as_uuid=True), nullable=False
    )
    created_date: datetime | Column[datetime] = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_date: datetime | Column[datetime] = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    def __init__(self) -> None:
        """Transaction Object Constructor."""

        self.id = uuid4()
        self.transaction_id = uuid4()
        self.salt_value = uuid4()

    def __str__(self) -> str:
        """String Representation of the Transaction Object."""

        return f"Transaction ID: {self.transaction_id}, Sender: {self.sender}, Receiver: {self.receiver}, Amount: {self.amount}, Title: {self.title}, Description: {self.description}, Transaction Status: {self.transaction_status}, Created Date: {self.created_date}, Updated Date: {self.updated_date}"

    def __repr__(self) -> str:
        """String Representation of the Transaction Object."""

        return f"Transaction({self.transaction_id}, {self.sender}, {self.receiver}, {self.amount}, {self.title}, {self.description}, {self.transaction_status}, {self.created_date}, {self.updated_date})"
