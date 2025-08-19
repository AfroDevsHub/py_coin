"""Cards: Serialiser for Card Model."""

from datetime import date, timedelta
from random import randint
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import validate_call
from config import AppConfig
from lib.interfaces.exceptions import CardValidationError
from lib.interfaces.warehouse.cards import CreateCardData, UpdateCardData
from lib.utils.constants.users import CardType, Regex
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from lib.utils.helpers.warehouse import generate_card
from models import ENGINE
from models.warehouse.cards import Card
from serialisers.serialiser import ISerialiser


class CardSerialiser(ISerialiser):
    """Serialiser for the Card Model."""

    __MAX_RETRIES = 3
    __CARD_VALID_YEARS = 365 * 5

    @validate_call
    def create(self, data: CreateCardData) -> Card:
        """CRUD Operation: Add Card."""

        with Session(ENGINE) as session:
            salt_value = uuid4()
            cvv_number = self.__get_cvv_number()

            expiration_date = date.today() + timedelta(days=self.__CARD_VALID_YEARS)
            card_number = self.__get_card_number(
                data.card_type, cvv_number, expiration_date
            )
            pin = str(get_hash_value(data.pin, str(salt_value)))
            card = Card(
                card_type=data.card_type,
                cvv_number=encrypt_data(cvv_number.encode()),
                expiration_date=expiration_date,
                card_number=encrypt_data(card_number.encode()),
                pin=pin,
                salt_value=salt_value,
            )

            try:
                session.add(card)
                session.commit()
                session.refresh(card)
            except IntegrityError as exc:
                raise CardValidationError("Card not Created.") from exc

            return card

    @validate_call
    def read(self, model_id: UUID) -> Card:
        """CRUD Operation: Get Card."""

        with Session(ENGINE) as session:
            card = session.get(Card, model_id)

            if not card:
                raise CardValidationError("Card not Found.")

            return card

    @validate_call
    def update(self, model_id: UUID, data: UpdateCardData) -> Card:
        """CRUD Operation: Update Card."""

        with Session(ENGINE) as session:
            card = session.get(Card, model_id)

            if card is None:
                raise CardValidationError("Card Not Found.")

            for key, value in data.model_dump().items():
                if key == "pin":
                    pin = str(get_hash_value(value, str(card.salt_value)))
                    setattr(card, "pin", pin)
                else:
                    setattr(card, "status", value)

            try:
                session.add(card)
                session.commit()
                session.refresh(card)
            except IntegrityError as exc:
                raise CardValidationError("Card not Created.") from exc

            return card

    @validate_call
    def delete(cls, model_id: UUID) -> str:
        """CRUD Operation: Delete Card."""

        with Session(ENGINE) as session:
            card = session.get(Card, model_id)

            if card is None:
                raise CardValidationError("Card Not Found.")

            try:
                session.delete(card)
                session.commit()
            except IntegrityError as exc:
                raise CardValidationError("Card not Deleted.") from exc

            return f"Deleted: {model_id}"

    def __get_card_number(
        self, card_type: CardType, cvv_number: str, expiration_date: date
    ) -> str:
        """Sets the Private Attribute."""

        for _ in range(self.__MAX_RETRIES):
            try:
                card_number = generate_card(card_type, cvv_number, expiration_date)
                return card_number
            except BaseException as e:
                print(f"Card Generator Failed: {e}")

        raise CardValidationError("Card Generator Error")

    def __get_cvv_number(self) -> str:
        """Sets the Private Attribute."""

        cvv_length = AppConfig().cvv_length
        cvv_number = "".join([str(randint(0, 9)) for _ in range(cvv_length)])

        if not Regex.CVV.value.match(cvv_number):
            raise CardValidationError("Invalid CVV.")

        return cvv_number
