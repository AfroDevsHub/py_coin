"""Blocks: validations for Block Related Models."""

from uuid import UUID
from sqlalchemy.orm import Session
from src.lib.types.exceptions import BlockError
from lib.utils.constants.blocks import BlockType
from models import ENGINE
from models.blockchain.blocks import Block


def validate_block_type(block_type: BlockType, **kwargs) -> BlockType:
    """Validates Block Type."""

    block = kwargs.get("model")
    if not isinstance(block, Block):
        raise BlockError("Invalid Type for this Attribute.")
    if not isinstance(block_type, BlockType):
        raise BlockError("Invalid Type for this Attribute.")
    if block.transaction_id:
        return BlockType.TRANSACTION
    if block.contract_id:
        return BlockType.CONTRACT
    return block_type


def validate_block_next(next_block_id: UUID, **kwargs) -> UUID:
    """Validates Next Block ID."""

    block = kwargs.get("model")
    if not isinstance(block, Block):
        raise BlockError("Invalid Type for this Attribute.")
    if block.next_block_id:
        raise BlockError("Invalid Block.")

    with Session(ENGINE) as session:
        next_block = session.get(Block, next_block_id)
        if not next_block:
            raise BlockError("Invalid Block.")
        if next_block.next_block_id:
            raise BlockError("Invalid Block.")
        if next_block_id == next_block.previous_block_id:
            raise BlockError("Invalid Block.")
    return next_block_id


def validate_block_previous(previous_block_id: UUID, **kwargs) -> UUID:
    """Validates Previous Block ID."""

    block = kwargs.get("model")
    if not isinstance(block, Block):
        raise BlockError("Invalid Type for this Attribute.")

    if block.next_block_id:
        raise BlockError("Invalid Block.")

    with Session(ENGINE) as session:
        previous_block = session.get(Block, previous_block_id)
        if not previous_block:
            raise BlockError("Invalid Block.")
        if previous_block.next_block_id:
            raise BlockError("Invalid Block.")

    return previous_block_id
