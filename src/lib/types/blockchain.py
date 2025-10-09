"""Data-Classes: Custom Data-Type Models."""

from pydantic import BaseModel

from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.transactions import TransactionStatus


class __TransactionData(BaseModel):
    """Typed Dictionary for Transaction Data."""

    title: str | None
    description: str | None
    amount: float | None
    transaction_status: TransactionStatus | None


class __ContractData(BaseModel):
    """Typed Dictionary for Contract Data."""

    title: str | None
    description: str | None
    contract: str | None
    contract_status: ContractStatus | None


class TransactionData(BaseModel):
    """Type Check for Transaction Data."""

    receiver_signiture: str
    sender_signiture: str
    data: "__TransactionData"


class ContractData(BaseModel):
    """Type Check for Contract Data."""

    contractor_signiture: str
    contractee_signiture: str
    data: "__ContractData"
