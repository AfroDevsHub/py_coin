"""Warehouse: Testing Card Serialiser."""

from datetime import date
import json
from re import compile as regex_regex_compile
import sys

from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from config import AppConfig
from lib.utils.encryption.encoders import get_hash_value
from serialisers.warehouse.cards import CardSerialiser
from lib.exceptions import CardValidationError, UserError
from lib.utils.constants.users import Status, CardType
from models import ENGINE
from models.warehouse.cards import Card
from services.authentication import AbstractService
from conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


@mark.parametrize("data", ["199715", "546789", "235968"])
def test_cardserialiser_create(data):
    """Testing Card Serialiser: Create Card."""

    for card_type in CardType:
        with Session(ENGINE) as session:
            card = CardSerialiser().create_card(card_type, data)
            card_id = AbstractService.get_public_id(card)
            card_data = (
                session.query(Card).filter(Card.card_id == card_id).one_or_none()
            )
            assert card_data.id is not None
            run_test_teardown([card_data], session)


@mark.parametrize("data", [199715, "def1223", "1991"])
def test_cardserialiser_create_invalid_card_type(data):
    """Testing Card Serialiser: Create Card."""

    for card_type in CardType:
        with raises((CardValidationError, DataError, ProgrammingError)):
            CardSerialiser().create_card(card_type, data)
    with raises((CardValidationError, DataError, ProgrammingError)):
        CardSerialiser().create_card("card_type", data)


def test_cardserialiser_get(get_cards):
    """Testing Card Serialiser: Get Card."""

    for card in get_cards:
        card = CardSerialiser().get_card(card.card_id)
        card_data = json.loads(AppConfig().fernet.decrypt(card.encode()).decode())

        assert isinstance(card_data, dict)
        for key in card_data:
            assert key not in Card.__EXCLUDE_ATTRIBUTES__


@mark.parametrize("data", check_invalid_ids())
def test_cardserialiser_get_invalid(data):
    """Testing Card Serialiser: Get Card."""

    with raises((CardValidationError, DataError, ProgrammingError)):
        CardSerialiser().get_card(data)


def test_cardserialiser_delete(get_cards):
    """Testing Card Serialiser: Delete Card."""

    for card in get_cards:
        assert CardSerialiser().delete_card(card.id).startswith("Deleted: ")


@mark.parametrize("data", check_invalid_ids())
def test_cardserialiser_delete_invalid(data):
    """Testing Card Serialiser: Delete Card."""

    with raises((CardValidationError, DataError, ProgrammingError)):
        CardSerialiser().delete_card(data)


@mark.parametrize(
    "data",
    [("199715", Status.ACTIVE), ("546789", Status.DELETED), ("235968", Status.NEW)],
)
def test_cardserialiser_update(get_cards, data):
    """Testing Card Serialiser: Update Card."""

    for card in get_cards:
        with Session(ENGINE) as session:
            pin = str(get_hash_value(data[0], str(card.salt_value)))
            CardSerialiser().update_card(card.id, pin=data[0], status=data[1])
            card = session.get(Card, card.id)
            assert card.id is not None
            assert card.pin == pin
            assert card.status == data[1]


@mark.parametrize(
    "data",
    [
        (None, Status.ACTIVE),
        ("123", Status.DISABLED),
        (123456, Status.NEW),
        ("123456", Status.INACTIVE),
        ("123456", None),
    ],
)
def test_cardserialiser_update_invalid(get_cards, data):
    """Testing Card Serialiser: Update Card."""

    for card in get_cards:
        with raises((CardValidationError, UserError, DataError, ProgrammingError)):
            CardSerialiser().update_card(card.id, pin=data[0], status=data[1])
