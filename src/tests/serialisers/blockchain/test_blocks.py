"""BlockChain: Testing Block Serialiser."""

from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

<<<<<<< HEAD
from config import AppConfig
from src.lib.types.exceptions import BlockError
=======
from lib.interfaces.exceptions import BlockError
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from lib.utils.constants.blocks import BlockType
from models.blockchain.blocks import Block
from serialisers.blockchain.blocks import BlockSerialiser
from models import ENGINE
from services.authentication import AbstractService
from conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


def test_transaction_blockserialiser_create(get_transactions):
    """Testing Block Serialiser: Create Block."""

    for transaction in get_transactions:
        with Session(ENGINE) as session:
            block_id = BlockSerialiser().create_block(transaction.id, None)
            block_id = AbstractService.get_public_id(block_id)
            block_data = (
                session.query(Block).filter(Block.block_id == block_id).one_or_none()
            )
            assert block_data.id is not None
            assert block_data.block_id is not None
            assert block_data.transaction_id is not None
            assert block_data.contract_id is None
            assert block_data.previous_block_id is None
            assert block_data.next_block_id is None
            assert block_data.block_type == BlockType.TRANSACTION

            run_test_teardown([block_data], session)

def test_contract_blockserialiser_create(get_contracts):
    """Testing Block Serialiser: Create Block."""

    for contract in get_contracts:
        with Session(ENGINE) as session:
            block_id = BlockSerialiser().create_block(None, contract.id)
            block_id = AbstractService.get_public_id(block_id)
            block_data = (
                session.query(Block).filter(Block.block_id == block_id).one_or_none()
            )
            assert block_data.id is not None
            assert block_data.block_id is not None
            assert block_data.transaction_id is None
            assert block_data.contract_id is not None
            assert block_data.previous_block_id is None
            assert block_data.next_block_id is None
            assert block_data.block_type == BlockType.CONTRACT

            run_test_teardown([block_data], session)

def test_unit_blockserialiser_create(get_contracts):
    """Testing Block Serialiser: Create Block."""

    for contract in get_contracts:
        with Session(ENGINE) as session:
            block_id = BlockSerialiser().create_block(None, None)
            block_id = AbstractService.get_public_id(block_id)
            block_data = (
                session.query(Block).filter(Block.block_id == block_id).one_or_none()
            )
            assert block_data.id is not None
            assert block_data.block_id is not None
            assert block_data.contract_id is None
            assert block_data.transaction_id is None
            assert block_data.previous_block_id is None
            assert block_data.next_block_id is None
            assert block_data.block_type == BlockType.UNIT

            run_test_teardown([block_data], session)

@mark.parametrize(
    "data",
    zip(check_invalid_ids(), list(reversed(check_invalid_ids()))),
)
def test_block_create_invalid(data):
    """Testing Contract Serialiser: Create Contract."""

    with raises((BlockError, DataError, ProgrammingError)):
        BlockSerialiser().create_block(data[0], data[1])


def test_blockileserialiser_get(get_blocks):
    """Testing Block Serialiser: Get Block."""

    for block in get_blocks:
        block_data = BlockSerialiser().get_block(block.block_id)

        assert isinstance(block_data, dict)
        for key in block_data:
            assert key not in block.__EXCLUDE_ATTRIBUTES__


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_blockliser_get_invalid(data):
    """Testing Block Serialiser: Get Block."""

    with raises((BlockError, DataError, ProgrammingError)):
        BlockSerialiser().get_block(data)


def test_blockserialiser_delete(get_blocks):
    """Testing Block Serialiser: Delete Block."""

    for block in get_blocks:
        assert BlockSerialiser().delete_block(block.id).startswith("Deleted: ")


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_blocker_delete_invalid(data):
    """Testing Block Serialiser: Delete Block."""

    with raises((BlockError, DataError, ProgrammingError)):
        BlockSerialiser().delete_block(data)


@mark.parametrize(
    "data",
    list(BlockType),
)
def test_block_update_valid_type(get_blocks, data):
    """Testing Block Serialiser: Update Block."""

    for block in get_blocks:
        with Session(ENGINE) as session:
            BlockSerialiser().update_block(
                block.id,
                block_type=data,
            )
            block_data = session.get(Block, block.id)
            assert block_data.id is not None
            assert block_data.block_type == data

@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_block_update_invalid_type(get_blocks, data):
    """Testing Block Serialiser: Update Block."""

    for block in get_blocks:
        with raises((BlockError, DataError, ProgrammingError)):
            BlockSerialiser().update_block(
                block.id,
                block_type=data,
            )

def test_block_update_valid_id(get_blocks):
    """Testing Block Serialiser: Update Block."""

    with Session(ENGINE) as session:
        BlockSerialiser().update_block(
            get_blocks[0].id, previous_block_id=get_blocks[1].id, next_block_id=get_blocks[2].id
        )
        block_data = session.get(Block, get_blocks[0].id)
        assert block_data.id is not None
        assert block_data.block_type == BlockType.UNIT
