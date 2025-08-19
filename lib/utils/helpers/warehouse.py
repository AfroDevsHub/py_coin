"""Cards: Serialiser for Card Model."""

from datetime import date
from random import randint
from sqlalchemy import Date, Enum, String, cast
from sqlalchemy.orm import Session
from pydantic import validate_call
from config import AppConfig
from lib.interfaces.exceptions import CardValidationError
from lib.utils.constants.users import CardType, Status
from models import ENGINE
from models.warehouse.cards import Card


@validate_call
def generate_card(card_type: CardType, cvv_number: str, expiration_date: date) -> str:
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
                cast(Card.status, Enum(Status, name="card_status")) != Status.INACTIVE,
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
