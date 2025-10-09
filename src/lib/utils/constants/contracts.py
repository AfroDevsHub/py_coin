"""Contracts: Contains Constants, Enumerations and Other Static data."""

from enum import Enum


class ContractStatus(Enum):
    """Enumeration of Contract Statuses."""

    DRAFT = "Draft"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    ACTIVE = "Active"
    CLOSED = "Closed"
