"""BlockChain: Testing Block Model."""

from pytest import raises

from sqlalchemy.orm import Session

from lib.utils.constants.blocks import BlockType
from models import ENGINE
from models.blockchain.blocks import Block
from conftest import run_test_teardown


def test_block_invalid_args() -> None:
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            block = Block("email", "password")
            session.add(block)
            session.commit()


def test_block_valid() -> None:
    """Testing a Valid Block Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        block = Block()
        block.block_type = BlockType.CONTRACT
        session.add(block)
        session.commit()

        assert block.id is not None
        assert block.block_type == BlockType.CONTRACT
        assert isinstance(block.to_dict(), dict)

        run_test_teardown([block], session)
