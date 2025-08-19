"""Blocks: Serialiser for Block Model."""

from typing import Any
from uuid import UUID
from pydantic import BaseModel, validate_call
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.interfaces.exceptions import BlockError
from lib.utils.constants.blocks import BlockType
from models import ENGINE
from models.blockchain.blocks import Block
from serialisers.serialiser import ISerialiser


class BlockData(BaseModel):
    """Data Model for Block."""

    block_type: str | None = None
    previous_block_id: UUID | None = None
    next_block_id: UUID | None = None


class BlockSerialiser(ISerialiser):
    """Serialiser for the Block Model."""

    @validate_call  # type: ignore
    def get_block(self, block_id: UUID) -> dict[str, Any]:
        """CRUD Operation: Read Block."""

        with Session(ENGINE) as session:
            query = select(Block).filter(cast(Block.block_id, uuid) == block_id)
            block = session.execute(query).scalar_one_or_none()

            if not block:
                raise BlockError("Block Not Found.")

            return self.__get_model_data__(block)

    @validate_call
    def create_block(
        self, transaction_id: UUID | None = None, contract_id: UUID | None = None
    ) -> str:
        """CRUD Operation: Create Block."""

        with Session(ENGINE) as session:
            if transaction_id:
                self.transaction_id = transaction_id
                self.block_type = BlockType.TRANSACTION

            if contract_id:
                self.contract_id = contract_id
                self.block_type = BlockType.CONTRACT

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise BlockError("Block Not Created." + str(exc)) from exc

            return str(self)

    @validate_call
    def update_block(self, private_id: str, data: BlockData) -> str:
        """CRUD Operation: Update Block."""

        with Session(ENGINE) as session:
            block = session.get(Block, private_id)

            if block is None:
                raise BlockError("Block Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(block, key, value)

            try:
                session.add(block)
                session.commit()
            except IntegrityError as exc:
                raise BlockError("Block Not Updated.") from exc

            return str(Block)

    @validate_call
    def delete_block(self, private_id: UUID) -> str:
        """CRUD Operation: Delete Block."""

        with Session(ENGINE) as session:
            block = session.get(Block, private_id)

            if not block:
                raise BlockError("Block Not Found")

            try:
                session.delete(block)
                session.commit()
            except IntegrityError as exc:
                raise BlockError("Block Not Deleted.") from exc

            return f"Deleted: {private_id}"
