"""Warehouse: Testing Cards Model."""

from datetime import date
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from lib.utils.constants.users import CardType
from models import ENGINE
from models.warehouse.cards import Card
from conftest import run_test_teardown


def test_card_invalid_no_args():
    """Testing Card With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            card = Card()
            session.add(card)
            session.commit()


def test_card_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            card = Card(CardType.CHEQUE)
            session.add(card)
            session.commit()


def test_card_valid():
    """Testing a Valid Card Constructor, with Required Arguments."""

    for key in CardType:
        with Session(ENGINE) as session:
            card = Card()
            card.card_number = "1991123456789"
            card.cvv_number = "123"
            card.card_type = key
            card.pin = "123456"
            card.expiration_date = date.today().replace(day=1)
            session.add(card)
            session.commit()

            assert card.id is not None
            assert card.salt_value is not None
            assert isinstance(card.to_dict(), dict)

            run_test_teardown([card], session)
