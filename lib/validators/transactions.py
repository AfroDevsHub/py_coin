"""Transactions: validations for Transaction Related Models."""

from lib.exceptions import TransactionError
from lib.utils.constants.transactions import TransactionStatus
from models.blockchain.transactions import Transaction


def validate_transaction_amount(amount: float, transaction: Transaction) -> float:
    """Validates Transaction Amount."""

    if amount <= 0.0:
        raise TransactionError("Invalid Transaction Amount.")

    if TransactionStatus(transaction.transaction_status) != TransactionStatus.DRAFT:
        raise TransactionError("Can not Update Agreed Amount.")

    return amount

def validate_transaction_status(
    status: TransactionStatus, transaction: Transaction
) -> TransactionStatus:
    """Validates Transaction Amount."""

    if TransactionStatus(transaction.transaction_status) == status:
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
        case _:
            raise TransactionError("Invalid Transaction Status.")
    raise TransactionError("Invalid Transaction Status.")
