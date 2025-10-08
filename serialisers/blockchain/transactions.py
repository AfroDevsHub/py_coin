"""Transactions: Serialiser for Transaction Model."""

from typing import Any
from uuid import UUID
from pydantic import BaseModel, validate_call
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

<<<<<<< HEAD
from lib.exceptions import TransactionError
=======
from lib.interfaces.exceptions import TransactionError
from lib.utils.constants.transactions import TransactionStatus
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from lib.utils.encryption.encoders import get_hash_value
from lib.validators.transactions import (
    validate_transaction_amount,
    validate_transaction_status,
)
from models import ENGINE
from models.blockchain.transactions import Transaction
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from serialisers.serialiser import ISerialiser


class UpdateTransactionData(BaseModel):
    """Data Model for Updating Transaction."""

    title: str | None = None
    description: str | None = None
    amount: float | None = None
    transaction_status: TransactionStatus | None = None


class TransactionSerialiser(ISerialiser):
    """Serialiser for the Transaction Model."""

<<<<<<< HEAD
    __SERIALISER_EXCEPTION__ = TransactionError
    __MUTABLE_KWARGS__: list[str] = [
        "title",
        "description",
        "amount",
        "transaction_status",
    ]

=======
    @validate_call
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
    def get_transaction(self, transaction_id: str) -> dict[str, Any]:
        """CRUD Operation: Read Transaction."""

        with Session(ENGINE) as session:
            query = select(Transaction).filter(
                cast(Transaction.transaction_id, uuid) == transaction_id
            )
            transaction = session.execute(query).scalar_one_or_none()

            if not transaction:
                raise TransactionError("Transaction Not Found.")

            return self.__get_model_data__(transaction)

    def create_transaction(self, sender: UUID, receiver: UUID, amount: float) -> str:
        """CRUD Operation: Create Transaction."""

        with Session(ENGINE) as session:
            sender_profile = session.get(PaymentProfile, sender)
            receiver_profile = session.get(PaymentProfile, receiver)
            if not sender_profile:
                raise TransactionError("Invalid Sender.")
            if not receiver_profile:
                raise TransactionError("Invalid Receiver.")

            self.sender = sender
            self.receiver = receiver
            self.amount = validate_transaction_amount(amount, self)

            sender_card = session.get(Card, sender_profile.card_id)
            receiver_card = session.get(Card, receiver_profile.card_id)

            if not sender_card:
                raise TransactionError("Invalid Sender Card Information.")
            if not receiver_card:
                raise TransactionError("Invalid Receiver Card Information.")

            self.sender_signiture = get_hash_value(
                str(sender_card.card_id),
                str(self.salt_value),
            )
            self.receiver_signiture = get_hash_value(
                str(receiver_card.card_id),
                str(self.salt_value),
            )

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise TransactionError("Transaction Not Created.") from exc

            return str(self)

    def update_transaction(
        self,
        private_id: str,
        sender_signiture: str,
        receiver_signiture: str,
        data: UpdateTransactionData,
    ) -> str:
        """CRUD Operation: Update Transaction."""

        with Session(ENGINE) as session:
            transaction = session.get(Transaction, private_id)

            if transaction is None:
                raise TransactionError("Transaction Not Found.")

            if str(transaction.sender_signiture) != sender_signiture:
                raise TransactionError("Sender Not Authorised.")
            if str(transaction.receiver_signiture) != receiver_signiture:
                raise TransactionError("Receiver Not Authorised.")

            for key, value in data.model_dump().items():
                if value is not None and key not in ["amount", "transaction_status"]:
                    setattr(transaction, key, value)

                if key == "amount":
                    transaction.amount = validate_transaction_amount(value, transaction)

                if key == "transaction_status":
                    transaction.transaction_status = validate_transaction_status(
                        value, transaction
                    )

            try:
                session.add(transaction)
                session.commit()
            except IntegrityError as exc:
                raise TransactionError("Transaction Not Updated.") from exc

            return str(transaction)

    def delete_transaction(self, private_id: str) -> str:
        """CRUD Operation: Delete Transaction."""

        with Session(ENGINE) as session:
            transaction = session.get(Transaction, private_id)

            if not transaction:
                raise TransactionError("Transaction Not Found")

            try:
                session.delete(transaction)
                session.commit()
            except IntegrityError as exc:
                raise TransactionError("Transaction Not Deleted.") from exc

            return f"Deleted: {private_id}"
