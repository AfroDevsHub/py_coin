"""Transactions: Contains Constants, Enumerations and Other Static data."""

from enum import Enum


class TransactionStatus(Enum):
    """Enumeration of Transaction Statuses."""

    DRAFT = "Transaction Drafted."
    APPROVED = "Transaction Approved."
    REJECTED = "Transaction Rejected."
    INSUFFICIENT = "Insufficient Funds."
    TRANSFERED = "Funds Transfered."
    REVERSED = "Transaction Reversed."
