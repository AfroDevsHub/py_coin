"""Test-Utils: Configure Block Chain Module."""

from uuid import UUID
from lib.utils.constants.contracts import ContractStatus
from lib.utils.constants.transactions import TransactionStatus
from lib.utils.encryption.encoders import get_hash_value
from models.blockchain.blocks import Block
from models.blockchain.contracts import Contract
from models.blockchain.transactions import Transaction


def create_transaction(
    sender: UUID,
    receiver: UUID,
    sender_card_id: str,
    receiver_card_id: str,
    status: TransactionStatus,
) -> Transaction:
    """Creates a Test Transaction."""

    transaction = Transaction()
    transaction.sender = sender
    transaction.receiver = receiver
    transaction.amount = 5.0
    transaction.sender_signiture = get_hash_value(
        sender_card_id, str(transaction.salt_value)
    )
    transaction.receiver_signiture = get_hash_value(
        receiver_card_id, str(transaction.salt_value)
    )
    transaction.transaction_status = status
    return transaction


def create_transactions(
    sender_ids: list[UUID],
    receiver_ids: list[UUID],
    sender_card_ids: list[str],
    receiver_card_ids: list[str],
) -> list[Transaction]:
    """Creates Test Transactions."""

    transactions = []
    statuses = [
        TransactionStatus.DRAFT,
        TransactionStatus.APPROVED,
        TransactionStatus.TRANSFERED,
    ]
    for sender_id, receiver_id, sender_card_id, receiver_card_id, status in zip(
        sender_ids, receiver_ids, sender_card_ids, receiver_card_ids, statuses
    ):
        transactions.append(
            create_transaction(
                sender_id, receiver_id, sender_card_id, receiver_card_id, status
            )
        )
    return transactions


def create_contract(
    contractor: UUID,
    contractee: UUID,
    contractor_card_id: str,
    contractee_card_id: str,
    status: ContractStatus,
) -> Contract:
    """Creates a Test Contract."""

    contract = Contract()
    contract.contract_id = get_hash_value(
        "Testing a string contract", str(contract.salt_value)
    )
    contract.contractor = contractor
    contract.contractee = contractee
    contract.contract = "Testing a string contract"
    contract.contractor_signiture = get_hash_value(
        contractor_card_id, str(contract.salt_value)
    )
    contract.contractee_signiture = get_hash_value(
        contractee_card_id, str(contract.salt_value)
    )
    contract.contract_status = status
    return contract


def create_contracts(
    contractor_ids: list[UUID],
    contractee_ids: list[UUID],
    contractor_card_ids: list[str],
    contractee_card_ids: list[str],
) -> list[Contract]:
    """Creates Test Contractss."""

    transactions = []
    statuses = [
        ContractStatus.DRAFT,
        ContractStatus.APPROVED,
        ContractStatus.CLOSED,
    ]
    for (
        contractor_id,
        contractee_id,
        contractor_card_id,
        contractee_card_id,
        status,
    ) in zip(
        contractor_ids,
        contractee_ids,
        contractor_card_ids,
        contractee_card_ids,
        statuses,
    ):
        transactions.append(
            create_contract(
                contractor_id,
                contractee_id,
                contractor_card_id,
                contractee_card_id,
                status,
            )
        )
    return transactions


def create_blocks() -> list[Block]:
    """Creates Test Blocks."""

    blocks = []
    for _ in range(3):
        blocks.append(Block())
    return blocks
