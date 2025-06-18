"""Transactions: validations for Transaction Related Models."""

from lib.exceptions import TransactionError
from lib.utils.constants.transactions import TransactionStatus
from models.blockchain.transactions import Transaction


def validate_transaction_amount(amount: float, **kwargs) -> float:
    """Validates Transaction Amount."""

    transaction = kwargs.get("model")
    if not isinstance(transaction, Transaction):
        raise TransactionError("Invalid Type for this Attribute.")
    if not isinstance(amount, float):
        raise TransactionError("Invalid Type for this Attribute.")
    if amount <= 0.0:
        raise TransactionError("Invalid Transaction Amount.")
    if (
        transaction.transaction_status
        and transaction.transaction_status != TransactionStatus.DRAFT
    ):
        raise TransactionError("Can not Update Agreed Amount.")
    return amount


def validate_transaction_status(
    status: TransactionStatus, **kwargs
) -> TransactionStatus:
    """Validates Transaction Amount."""

    transaction = kwargs.get("model")
    if not isinstance(transaction, Transaction):
        raise TransactionError("Invalid Type for this Attribute.")
    if not isinstance(status, TransactionStatus):
        raise TransactionError("Invalid Type for this Attribute.")
    if transaction.transaction_status == status:
        return status
    match (transaction.transaction_status):
        case TransactionStatus.DRAFT:
            if status in [
                TransactionStatus.APPROVED,
                TransactionStatus.REJECTED,
            ]:
                return status
        case TransactionStatus.APPROVED:
            if status in [
                TransactionStatus.INSUFFICIENT,
                TransactionStatus.TRANSFERED,
            ]:
                return status
        case TransactionStatus.TRANSFERED:
            if status == TransactionStatus.REVERSED:
                return status
        case None:
            return TransactionStatus.DRAFT
        case _:
            raise TransactionError("Invalid Transaction Status.")
    raise TransactionError("Invalid Transaction Status.")
