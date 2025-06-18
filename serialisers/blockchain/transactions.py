"""Transactions: Serialiser for Transaction Model."""

from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.exceptions import TransactionError
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.blockchain.transactions import Transaction
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from serialisers.serialiser import BaseSerialiser


class TransactionSerialiser(Transaction, BaseSerialiser):
    """Serialiser for the Transaction Model."""

    __SERIALISER_EXCEPTION__ = TransactionError
    __MUTABLE_KWARGS__: list[str] = [
        "title",
        "description",
        "amount",
        "transaction_status",
    ]

    def get_transaction(self, transaction_id: str) -> dict:
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
            self.amount = self.validate_serialiser_kwargs("amount", amount, model=self)

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
        self, private_id: str, sender_signiture: str, receiver_signiture: str, **kwargs
    ) -> str:
        """CRUD Operation: Update Transaction."""

        with Session(ENGINE) as session:
            transaction = session.get(Transaction, private_id)

            if transaction is None:
                raise TransactionError("Transaction Not Found.")

            if transaction.sender_signiture != sender_signiture:
                raise TransactionError("Sender Not Authorised.")
            if transaction.receiver_signiture != receiver_signiture:
                raise TransactionError("Receiver Not Authorised.")

            for key, value in kwargs.items():
                if key not in TransactionSerialiser.__MUTABLE_KWARGS__:
                    raise TransactionError("Invalid Transaction.")
                if value != getattr(transaction, key):
                    value = self.validate_serialiser_kwargs(key, value, model=transaction)
                    setattr(transaction, key, value)

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
