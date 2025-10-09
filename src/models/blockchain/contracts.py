"""Contracts: Contract Model."""

from datetime import datetime
from uuid import uuid4, UUID as uuid

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    text,
)

from src.lib.utils.constants.contracts import ContractStatus
from src.models import Base


class Contract(Base):
    """Model representing a Contract."""

    __tablename__ = "contracts"
    __table_args__ = ({"schema": "blockchain"},)

    id: uuid | Column[uuid] = Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False
    )
    contract_id: str | Column[str] = Column("contract_id", String(256), nullable=False)
    contractor: uuid | Column[uuid] = Column(
        "contractor",
        UUID(as_uuid=True),
        ForeignKey("users.payment_profiles.id"),
        nullable=False,
    )
    contractee: uuid | Column[uuid] = Column(
        "contractee",
        UUID(as_uuid=True),
        ForeignKey("users.payment_profiles.id"),
        nullable=False,
    )
    title: str | Column[str] = Column("title", String(256), nullable=False)
    description: str | Column[str] = Column("description", String(256), nullable=False)
    contract: str | Column[str] = Column("contract", String, nullable=False)
    contract_status: ContractStatus | Column[ContractStatus] = Column(
        "contract_status",
        Enum(ContractStatus, name="contract_status"),
        nullable=False,
        default=ContractStatus.DRAFT,
    )
    contractor_signiture: str | Column[str] = Column(
        "contractor_signiture", String(256), nullable=False
    )
    contractee_signiture: str | Column[str] = Column(
        "contractee_signiture", String(256), nullable=True
    )
    salt_value: uuid | Column[uuid] = Column("salt_value", UUID(as_uuid=True), nullable=False)
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
        self.salt_value = uuid4()

    def __str__(self) -> str:
        """String Representation of the Contract Object."""

        return f"Contract ID: {self.contract_id}, Contractor: {self.contractor}, Contractee: {self.contractee}, Title: {self.title}, Description: {self.description}, Contract Status: {self.contract_status}, Created Date: {self.created_date}, Updated Date: {self.updated_date}"

    def __repr__(self) -> str:
        """String Representation of the Contract Object."""

        return f"Contract({self.contract_id}, {self.contractor}, {self.contractee}, {self.title}, {self.description}, {self.contract_status}, {self.created_date}, {self.updated_date})"
