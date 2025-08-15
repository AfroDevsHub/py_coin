"""Cards: Serialiser for Card Model."""

from datetime import date, timedelta
from random import randint
from uuid import UUID
from sqlalchemy import Column, Date, Enum, String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, field_validator, validate_call
from config import AppConfig
from lib.interfaces.exceptions import CardValidationError
from lib.utils.constants.users import CardType, DateFormat, Regex, Status
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from lib.validators.users import (
    validate_cvv_number,
)
from models import ENGINE
from models.warehouse.cards import Card
from serialisers.serialiser import BaseSerialiser


class CreateCardData(BaseModel):
    card_type: CardType
    pin: str

    @field_validator("pin")
    def validate_pin(cls, value: str) -> str:
        if not Regex.PIN.value.match(value):
            raise CardValidationError("Invalid Pin")

        return value


class UpdateCardData(BaseModel):
    status: Status | None = None
    pin: str | None = None

    @field_validator("pin")
    def validate_pin(cls, value: str) -> str:
        if not Regex.PIN.value.match(value):
            raise CardValidationError("Invalid Pin")

        return value

    @field_validator("status")
    def validate_status(cls, value: Status) -> Status:
        """Validate Account Status."""

        if value not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
            raise CardValidationError("Invalid Status.")

        return value


class CardSerialiser(Card, BaseSerialiser):
    """Serialiser for the Card Model."""

    __SERIALISER_EXCEPTION__ = CardValidationError
    __MUTABLE_KWARGS__: list[str] = ["status", "pin"]
    __MAX_RETRIES__ = 3
    __CARD_VALID_YEARS__ = 365 * 5

    @validate_call
    def get_card(self, card_id: UUID) -> str:
        """CRUD Operation: Get Card."""

        with Session(ENGINE) as session:
            query = select(Card).filter(cast(Card.card_id, String) == card_id)
            card = session.execute(query).scalar_one_or_none()

            if not card:
                raise CardValidationError("Card not Found.")

            return self.__get_encrypted_model_data__(card)

    @validate_call
    def create_card(self, data: CreateCardData) -> str:
        """CRUD Operation: Add Card."""

        with Session(ENGINE) as session:
            self.card_type = data.card_type
            self.cvv_number = str(self.__get_cvv_number__())
            self.expiration_date = (
                date.today() + timedelta(days=self.__CARD_VALID_YEARS__)
            ).replace(day=1)
            self.card_number = str(self.__get_card_number__())
            self.pin = str(self.__get_pin__(data.pin, str(self.salt_value)))
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

    @validate_call
    def update_card(self, private_id: str, data: UpdateCardData) -> str:
        """CRUD Operation: Update Card."""

        with Session(ENGINE) as session:
            card = session.get(Card, private_id)

            if card is None:
                raise CardValidationError("Card Not Found.")

            if data.pin:
                valid_pin = self.__get_pin__(data.pin, str(card.salt_value))
                setattr(card, "pin", valid_pin)
            if data.status:
                setattr(card, "status", data.status)

            try:
                session.add(card)
                session.commit()
            except IntegrityError as exc:
                raise CardValidationError("Card not Created.") from exc

            return str(card)

    @validate_call
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

        for _ in range(self.__MAX_RETRIES__):
            try:
                card_number = self.generate_card(
                    self.card_type, self.cvv_number, self.expiration_date
                )
                return encrypt_data(str(card_number).encode())
            except BaseException as e:
                print(f"Card Generator Failed: {e}")
        
        raise CardValidationError("Card Generator Error")
    

    def __get_pin__(self, pin: str, salt_value: str) -> str:
        """Sets Valid Card Pin."""

        return str(get_hash_value(pin, salt_value))

    def __get_cvv_number__(self) -> str:
        """Sets the Private Attribute."""

        cvv_length = AppConfig().cvv_length
        cvv_number = "".join([str(randint(0, 9)) for _ in range(cvv_length)])
        cvv_number = validate_cvv_number(cvv_number)
        return encrypt_data(cvv_number.encode())

    @validate_call
    @staticmethod
    def generate_card(
        card_type: CardType | Column[CardType],
        cvv_number: str | Column[str],
        expiration_date: date | Column[date],
    ) -> str:
        """Generates a Valid Card."""

        card_length = AppConfig().card_length
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

    @validate_call
    @staticmethod
    def get_card_id(
        cvv_number: str,
        card_number: str,
        expiration_date: date | Column[date],
    ) -> str:
        """Sets Valid Card ID."""

        salt_value = AppConfig().salt_value
        return str(
            get_hash_value(
                card_number
                + cvv_number
                + expiration_date.strftime(DateFormat.SHORT.value),
                str(salt_value),
            )
        )
