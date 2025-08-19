"""Cards: Card Model."""

from datetime import date
from uuid import uuid4
from sqlalchemy import UUID, Column, Date, DateTime, Enum, String, text
from lib.utils.constants.users import CardType, Status
from models import Base


class Card(Base):
    """Model representing an Account Card."""

    __tablename__ = "cards"
    __table_args__ = ({"schema": "warehouse"},)

    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    card_id = Column(
        "card_id",
        String(256),
        nullable=False,
        default=uuid4,
        unique=True,
    )
    card_number = Column("card_number", String(256), nullable=False)
    cvv_number = Column("cvv_number", String(256), nullable=False)
    card_type: CardType | Column[CardType] = Column(
        "card_type", Enum(CardType, name="card_type"), nullable=False
    )
    status: Status | Column[Status] = Column(
        "status", Enum(Status, name="card_status"), nullable=False, default=Status.NEW
    )
    pin = Column("pin", String(256), nullable=False)
    expiration_date: date | Column[date] = Column(
        "expiration_date", Date, nullable=False
    )
    salt_value = Column("salt_value", UUID(as_uuid=True), nullable=False)
    created_date = Column(
        "created_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
    )
    updated_date = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __str__(self) -> str:
        """String Representation of the Card Object."""

        return f"Card ID: {self.card_id}, Card Number: {self.card_number}, Card Type: {self.card_type}, Status: {self.status}, Expiration Date: {self.expiration_date}"

    def __repr__(self) -> str:
        """String Representation of the Card Object."""

        return f"Card({self.card_id}, {self.card_number}, {self.card_type}, {self.status}, {self.expiration_date})"
