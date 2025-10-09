"""Blocks: Contains Constants, Enumerations and Other Static data."""

from enum import Enum


class BlockType(Enum):
    """Enumeration of Block Types."""

    TRANSACTION = "Transaction Block"
    CONTRACT = "Contract Block"
    UNIT = "Unit Block"
