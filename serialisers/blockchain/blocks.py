"""Blocks: Serialiser for Block Model."""

from typing import Any, Optional
from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.exceptions import BlockError
from lib.validators.blocks import validate_block_next, validate_block_previous
from models import ENGINE
from models.blockchain.blocks import Block
from serialisers.serialiser import BaseSerialiser


class BlockSerialiser(Block, BaseSerialiser):
    """Serialiser for the Block Model."""

    __SERIALISER_EXCEPTION__ = BlockError
    __MUTABLE_KWARGS__: list[str] = ["block_type", "previous_block_id", "next_block_id"]

    def get_block(
        self,
        block_id: Optional[UUID] = None,
        transaction_id: Optional[UUID] = None,
        contract_id: Optional[UUID] = None,
    ) -> dict[str, Any]:
        """CRUD Operation: Read Block."""

        with Session(ENGINE) as session:
            if block_id:
                query = select(Block).filter(cast(Block.block_id, uuid) == block_id)
            elif transaction_id:
                query = select(Block).filter(
                    cast(Block.transaction_id, uuid) == transaction_id
                )
            else:
                query = select(Block).filter(
                    cast(Block.contract_id, uuid) == contract_id
                )
            block = session.execute(query).scalar_one_or_none()

            if not block:
                raise BlockError("Block Not Found.")
            return self.__get_model_data__(block)

    def create_block(
        self,
        transaction_id: Optional[UUID] = None,
        contract_id: Optional[UUID] = None,
    ) -> str:
        """CRUD Operation: Create Block."""

        with Session(ENGINE) as session:
            if transaction_id:
                self.transaction_id = transaction_id
            if contract_id:
                self.contract_id = contract_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise BlockError("Block Not Created." + str(exc)) from exc

            return str(self)

    def update_block(
        self,
        private_id: str,
        **kwargs,
    ) -> str:
        """CRUD Operation: Update Block."""

        with Session(ENGINE) as session:
            block = session.get(Block, private_id)

            if block is None:
                raise BlockError("Block Not Found.")

            for key, value in kwargs.items():
                if key not in BlockSerialiser.__MUTABLE_KWARGS__:
                    raise BlockError("Invalid Block.")
                value = self.validate_serialiser_kwargs(key, value, model=block)
                setattr(block, key, value)

            try:
                session.add(block)
                session.commit()
            except IntegrityError as exc:
                raise BlockError("Block Not Updated.") from exc

            return str(Block)

    def delete_block(self, private_id: str) -> str:
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
