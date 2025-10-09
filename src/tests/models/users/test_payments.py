"""Users: Testing Payments Profile Model."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.utils.constants.users import Status
from models import ENGINE
from models.user.payments import PaymentProfile
from conftest import run_test_teardown


def test_user_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            payment_profile = PaymentProfile()
            session.add(payment_profile)
            session.commit()


def test_payment_profile_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            payment_profile = PaymentProfile("email", "password")
            session.add(payment_profile)
            session.commit()


def test_payment_profile_valid(get_accounts, get_cards):
    """Testing a Valid User Constructor, with Required Arguments."""

    for account, card in zip(get_accounts, get_cards):
        with Session(ENGINE) as session:
            payment_profile = PaymentProfile()
            payment_profile.card_id = card.id
            payment_profile.account_id = account.id
            payment_profile.name = "Delali Funani Test Profile"
            payment_profile.description = (
                "Longer Description of the Delali Funani Test Profile"
            )
            session.add(payment_profile)
            session.commit()

            assert payment_profile.id is not None
            assert payment_profile.balance == 0.0
            assert payment_profile.status == Status.NEW

            run_test_teardown([payment_profile], session)
