"""User: Testing Payments Profile Serialiser."""

from uuid import uuid4
from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from lib.utils.constants.users import Status
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from serialisers.user.payments import PaymentProfileSerialiser
from lib.exceptions import PaymentProfileError
from models import ENGINE
from services.authentication import AbstractService
from conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


def test_paymentprofileserialiser_create(get_accounts, get_cards):
    """Testing PaymentProfile Serialiser: Create PaymentProfile."""

    for account, card in zip(get_accounts, get_cards):
        with Session(ENGINE) as session:
            payment_profile = PaymentProfileSerialiser().create_payment_profile(
                account.id, card.id
            )
            payment_id = AbstractService.get_public_id(payment_profile)
            payment = (
                session.query(PaymentProfile)
                .filter(PaymentProfile.payment_id == payment_id)
                .one_or_none()
            )
            assert payment.id is not None
            run_test_teardown([payment], session)


@mark.parametrize("data", check_invalid_ids())
def test_paymentprofileserialiser_create_inavild_private_id(data):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises((PaymentProfileError, DataError, ProgrammingError)):
        PaymentProfileSerialiser().create_payment_profile(data, data)


def test_paymentprofileserialiser_get(get_payments):
    """Testing PaymentProfile Serialiser: Get PaymentProfile."""

    for payment in get_payments:
        payment_data = PaymentProfileSerialiser().get_payment_profile(
            payment.payment_id
        )

        assert isinstance(payment_data, dict)
        for key in payment_data:
            assert key not in Account.__EXCLUDE_ATTRIBUTES__


@mark.parametrize("data", check_invalid_ids())
def test_paymentprofileserialiser_get_inavild_private_id(data):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises((PaymentProfileError, DataError, ProgrammingError)):
        assert PaymentProfileSerialiser().get_payment_profile(data)


def test_paymentprofileserialiser_delete(get_payments):
    """Testing PaymentProfile Serialiser: Delete PaymentProfile."""

    for payment in get_payments:
        assert (
            PaymentProfileSerialiser()
            .delete_payment_profile(payment.id)
            .startswith("Deleted: ")
        )


@mark.parametrize("data", check_invalid_ids())
def test_paymentprofileserialiser_delete_inavild_private_id(data):
    """Testing PaymentProfile Serialiser: Create PaymentProfile Invalid [Card ID]."""

    with raises((PaymentProfileError, DataError, ProgrammingError)):
        assert PaymentProfileSerialiser().delete_payment_profile(data)


@mark.parametrize(
    "data",
    [
        {
            "balance": 5.0,
            "name": "Well described name for profile",
            "description": "Longer Description - Well described name for profile.",
            "status": Status.ACTIVE,
        },
        {
            "balance": 500.0,
            "status": Status.NEW,
        },
        {
            "status": Status.DELETED,
        },
    ],
)
def test_paymentprofileserialiser_update_valid(get_payments, data):
    """Testing PaymentProfile Serialiser: Update PaymentProfile."""

    for payment in get_payments:
        with Session(ENGINE) as session:
            PaymentProfileSerialiser().update_payment_profile(payment.id, **data)
            payment = session.get(PaymentProfile, payment.id)
            assert payment.id is not None
            for key, value in data.items():
                assert getattr(payment, key) == value


@mark.parametrize(
    "data",
    [
        {
            "balance": -5.0,
            "name": "Well described name for profile",
            "description": "Longer Description - Well described name for profile.",
            "status": Status.ACTIVE,
        },
        {
            "balance": 0.0,
            "status": Status.DISABLED,
            "name": 1,
            "description": 1,
        },
        {
            "balance": "0.0",
            "status": Status.INACTIVE,
        },
        {
            "balance": None,
            "name": "Well",
            "description": "Longe",
            "status": "Status.ACTIVE",
        },
        {
            "name": None,
            "description": None,
            "status": None,
        },
    ],
)
def test_paymentprofileserialiser_update_invalid(get_payments, data):
    """Testing PaymentProfile Serialiser: Invalid Update PaymentProfile."""

    for payment in get_payments:
        with raises(PaymentProfileError):
            PaymentProfileSerialiser().update_payment_profile(payment.id, **data)
