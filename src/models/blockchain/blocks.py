"""Blockss: Block Model."""

from datetime import datetime
from uuid import uuid4, UUID as uuid

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    text,
)

from src.lib.utils.constants.blocks import BlockType
from src.models import Base


class Block(Base):
    """Model representing a Block."""

    __tablename__ = "blocks"
    __table_args__ = ({"schema": "blockchain"},)

    id: uuid | Column[uuid] = Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False
    )
    block_id: uuid | Column[uuid] = Column(
        "block_id", UUID(as_uuid=True), nullable=False
    )
    transaction_id: uuid | Column[uuid] = Column(
        "transaction_id",
        UUID(as_uuid=True),
        ForeignKey("blockchain.transactions.id"),
        nullable=True,
    )
    contract_id: uuid | Column[uuid] = Column(
        "contract_id",
        UUID(as_uuid=True),
        ForeignKey("blockchain.contracts.id"),
        nullable=True,
    )
    previous_block_id: uuid | Column[uuid] = Column(
        "previous_block_id", UUID(as_uuid=True), nullable=True
    )
    next_block_id: uuid | Column[uuid] = Column(
        "next_block_id", UUID(as_uuid=True), nullable=True
    )
    block_type: BlockType | Column[BlockType] = Column(
        "block_type",
        Enum(BlockType, name="block_type"),
        nullable=False,
        default=BlockType.UNIT,
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
        """Contract Object Constructor."""

        self.id = uuid4()
        self.block_id = uuid4()

    def __str__(self) -> str:
        """String Representation of the Contract Object."""

        return f"Block ID: {self.block_id}, Transaction ID: {self.transaction_id}, Contract ID: {self.contract_id}, Previous Block ID: {self.previous_block_id}, Next Block ID: {self.next_block_id}, Block Type: {self.block_type}, Created Date: {self.created_date}, Updated Date: {self.updated_date}"

    def __repr__(self) -> str:
        """String Representation of the Contract Object."""

        return f"Block({self.block_id}, {self.transaction_id}, {self.contract_id}, {self.previous_block_id}, {self.next_block_id}, {self.block_type}, {self.created_date}, {self.updated_date})"
