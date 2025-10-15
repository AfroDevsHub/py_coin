"""Blockchain: BlockChain Services."""

from typing import Optional
from uuid import UUID
from lib.decorators.utils import validate_function_signature
from src.lib.types.exceptions import BlockError
from src.lib.types.responses import ServiceResponse
from lib.types.blockchain import ContractData, TransactionData
from lib.utils.constants.blocks import BlockType
from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.responses import ServiceStatus
from lib.utils.constants.transactions import TransactionStatus
from serialisers.blockchain.blocks import BlockSerialiser
from serialisers.blockchain.contracts import ContractSerialiser
from serialisers.blockchain.transactions import TransactionSerialiser


class BlockChainService:
    """Manages BlockChain Operations."""

    __instance = None
    CHAIN: list[dict] = []

    def __new__(cls) -> "BlockChainService":
        """Singleton Class Constructor."""

        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def append_block_chain(cls, block_id: UUID) -> ServiceResponse:
        """Appends a Block."""

        block = BlockSerialiser().get_block(block_id)
        previous_block: Optional[dict] = None

        if not block["transaction_id"] and not block["contract_id"]:
            raise BlockError("Invalid Transaction Block.")

        if cls.CHAIN:
            previous_block = BlockSerialiser().get_block(
                UUID(cls.CHAIN[-1]["block_id"])
            )
            
        if previous_block:
            BlockSerialiser().update_block(
                block["id"], previous_block_id=UUID(previous_block["id"])
            )
            BlockSerialiser().update_block(
                previous_block["id"], next_block_id=UUID(block["id"])
            )

        cls.CHAIN.append(block)

        block = BlockSerialiser().get_block(block["block_id"])
        if previous_block:
            previous_block = BlockSerialiser().get_block(previous_block["block_id"])

        data = {"block": block, "previous_block": previous_block}
        return ServiceResponse("Block Chain Updated.", ServiceStatus.SUCCESS, data=data)

    @classmethod
    def create_transaction(
        cls, sender: UUID, receiver: UUID, transaction_amount: float
    ) -> ServiceResponse:
        """Creates a New Transaction Block."""

        response = TransactionSerialiser().create_transaction(
            sender, receiver, amount=transaction_amount
        )
        transaction_id = response.split(" ")[-1]
        transaction = TransactionSerialiser().get_transaction(transaction_id)
        return ServiceResponse(
            "Transaction Block Created Successfully.",
            ServiceStatus.SUCCESS,
            data=transaction,
        )

    @classmethod
    def create_contract(
        cls, contractor: UUID, contractee: UUID, contract_data: str
    ) -> ServiceResponse:
        """Creates a New Transaction Block."""

        response = ContractSerialiser().create_contract(
            contractor, contractee, contract_data
        )
        contract_id = response.split(" ")[-1]
        contract = ContractSerialiser().get_contract(contract_id)
        return ServiceResponse(
            "Contract Block Created Successfully.", ServiceStatus.SUCCESS, data=contract
        )

    @classmethod
    def update_transaction(
        cls,
        transaction_id: UUID,
        sender_signiture: str,
        receiver_signiture: str,
        transaction_data: TransactionData,
    ) -> ServiceResponse:
        """Approve a Given Transaction."""

        data = {}
        response = TransactionSerialiser().update_transaction(
            transaction_id,
            sender_signiture,
            receiver_signiture,
            **transaction_data,
        )
        transaction_id = response.split(" ")[-1]
        transaction = TransactionSerialiser().get_transaction(transaction_id)
        data.update({"transaction": transaction})
        if transaction_data["transaction_status"] == TransactionStatus.APPROVED:
            block = cls.__create_new_block__(transaction_id=transaction["id"])
            data.update({"block": block})
        return ServiceResponse(
            "Transaction Block Created Successfully.",
            ServiceStatus.SUCCESS,
            data=data,
        )

    @classmethod
    def update_contract(
        cls,
        contract_id: UUID,
        contractor_signiture: str,
        contractee_signiture: str,
        contract_data: ContractData,
    ) -> ServiceResponse:
        """Approve a Given Contract."""

        data = {}
        response = ContractSerialiser().update_contract(
            contract_id,
            contractor_signiture,
            contractee_signiture,
            **contract_data,
        )
        contract_id = response.split(" ")[-1]
        contract = ContractSerialiser().get_contract(contract_id)
        data.update({"contract": contract})
        if contract_data["contract_status"] == ContractStatus.APPROVED:
            block = cls.__create_new_block__(contract_id=contract["id"])
            data.update({"block": block})
        return ServiceResponse(
            "Contract Block Created Successfully.", ServiceStatus.SUCCESS, data=data
        )

    @classmethod
    def __create_new_block__(
        cls, transaction_id: Optional[UUID] = None, contract_id: Optional[UUID] = None
    ) -> dict[str, Any]:
        """Creates a New Block - Transaction or Contract."""

        if transaction_id and contract_id:
            raise BlockError("Invalid Block - Transaction or Contract not both.")

        response = BlockSerialiser().create_block(transaction_id, contract_id)
        block_id = response.split(" ")[-1]
        block = BlockSerialiser().get_block(block_id)
        if transaction_id:
            BlockSerialiser().update_block(
                block["id"], block_type=BlockType.TRANSACTION
            )

        if contract_id:
            BlockSerialiser().update_block(block["id"], block_type=BlockType.CONTRACT)

        return BlockSerialiser().get_block(block_id)
