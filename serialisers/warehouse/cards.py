"""Cards: Serialiser for Card Model."""

from datetime import date, timedelta
from random import randint
from uuid import UUID
from sqlalchemy import Column, Date, Enum, String, cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config import AppConfig
from lib.exceptions import CardValidationError
from lib.utils.constants.users import CardType, DateFormat, Status
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from lib.validators.users import (
    validate_card_number,
    validate_card_type,
    validate_cvv_number,
    validate_pin,
)
from models import ENGINE
from models.warehouse.cards import Card
from serialisers.serialiser import BaseSerialiser


class CardSerialiser(Card, BaseSerialiser):
    """Serialiser for the Card Model."""

    __SERIALISER_EXCEPTION__ = CardValidationError
    __MUTABLE_KWARGS__: list[str] = ["status", "pin"]
    __MAX_RETRIES__ = 3
    __CARD_VALID_YEARS__ = 365 * 5

    def get_card(self, card_id: UUID) -> str:
        """CRUD Operation: Get Card."""

        with Session(ENGINE) as session:
            query = select(Card).filter(cast(Card.card_id, String) == card_id)
            card = session.execute(query).scalar_one_or_none()

            if not card:
                raise CardValidationError("Card not Found.")

            return self.__get_encrypted_model_data__(card)

    def create_card(self, card_type: CardType, pin: str) -> str:
        """CRUD Operation: Add Card."""

        with Session(ENGINE) as session:
            card_type = validate_card_type(card_type)
            self.card_type = card_type
            self.cvv_number = str(self.__get_cvv_number__())
            self.expiration_date = (
                date.today() + timedelta(days=self.__CARD_VALID_YEARS__)
            ).replace(day=1)
            self.card_number = str(self.__get_card_number__())
            self.pin = str(self.__get_pin__(pin, str(self.salt_value)))
            self.card_id = str(
                self.get_card_id(
                    str(decrypt_data(str(self.cvv_number))),
                    str(decrypt_data(str(self.card_number))),
                    self.expiration_date,
                )
            )
            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise CardValidationError("Card not Created.") from exc

            return str(self)

    def update_card(self, private_id: UUID, **kwargs) -> str:
        """CRUD Operation: Update Card."""

        with Session(ENGINE) as session:
            card = session.get(Card, private_id)

            if card is None:
                raise CardValidationError("Card Not Found.")

            for key, value in kwargs.items():
                if key not in CardSerialiser.__MUTABLE_KWARGS__:
                    raise CardValidationError("Invalid attribute to Update.")

                if key == "pin":
                    valid_pin = self.__get_pin__(value, str(card.salt_value))
                    setattr(card, key, valid_pin)
                if key == "status":
                    value = self.validate_serialiser_kwargs(key, value)
                    setattr(card, key, value)

            try:
                session.add(card)
                session.commit()
            except IntegrityError as exc:
                raise CardValidationError("Card not Created.") from exc

            return str(card)

    @classmethod
    def delete_card(cls, private_id: UUID) -> str:
        """CRUD Operation: Delete Card."""

        with Session(ENGINE) as session:
            card = session.get(Card, private_id)

            if card is None:
                raise CardValidationError("Card Not Found.")

            try:
                session.delete(card)
                session.commit()
            except IntegrityError as exc:
                raise CardValidationError("Card not Deleted.") from exc

            return f"Deleted: {private_id}"

    def __get_card_number__(self) -> str:
        """Sets the Private Attribute."""

        for retries in range(self.__MAX_RETRIES__):
            try:
                card_number = self.generate_card(
                    self.card_type, self.cvv_number, self.expiration_date
                )
                break
            except CardValidationError:
                if retries == self.__MAX_RETRIES__ - 1:
                    raise

        card_number = validate_card_number(str(card_number))
        return encrypt_data(str(card_number).encode())

    def __get_pin__(self, pin: str, salt_value: str) -> str:
        """Sets Valid Card Pin."""

        pin = validate_pin(pin)
        return str(get_hash_value(pin, salt_value))

    def __get_cvv_number__(self) -> str:
        """Sets the Private Attribute."""

        cvv_length = AppConfig().cvv_length
        if not isinstance(cvv_length, int):
            raise CardValidationError("Invalid CVV Number Length")
        cvv_number = "".join([str(randint(0, 9)) for _ in range(cvv_length)])
        cvv_number = validate_cvv_number(cvv_number)
        return encrypt_data(cvv_number.encode())

    @staticmethod
    def generate_card(
        card_type: CardType | Column[CardType],
        cvv_number: str | Column[str],
        expiration_date: date | Column[date],
    ) -> str:
        """Generates a Valid Card."""

        card_length = AppConfig().card_length
        if not isinstance(card_length, int):
            raise CardValidationError("Invalid Card Number Length.")
        card_number = "".join(
            [str(randint(0, 9)) for _ in range(card_length - len(card_type.value[1]))]
        )
        card_number = card_type.value[1] + card_number
        with Session(ENGINE) as session:
            cards_count = (
                session.query(Card)
                .filter(
                    cast(Card.status, Enum(Status, name="card_status"))
                    != Status.INACTIVE,
                    cast(Card.card_number, String) == card_number,
                    cast(Card.card_type, Enum(CardType, name="card_type")) == card_type,
                    cast(Card.cvv_number, String) == cvv_number,
                    cast(Card.expiration_date, Date) == expiration_date,
                )
                .count()
            )
            if cards_count != 0:
                raise CardValidationError("Card Number Already Exists.")
            return card_number

    @staticmethod
    def get_card_id(
        cvv_number: str,
        card_number: str,
        expiration_date: date | Column[date],
    ) -> str:
        """Sets Valid Card ID."""

        salt_value = AppConfig().salt_value
        if not isinstance(salt_value, UUID):
            raise CardValidationError("Invalid Card Information.")
        return str(
            get_hash_value(
                card_number
                + cvv_number
                + expiration_date.strftime(DateFormat.SHORT.value),
                str(salt_value),
            )
        )
