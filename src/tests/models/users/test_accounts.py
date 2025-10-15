"""Users: Testing Account Model."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.utils.constants.users import Status
from models import ENGINE
from models.user.accounts import Account
from models.user.profiles import UserProfile
from conftest import run_test_teardown


def test_account_invalid_no_args() -> None:
    """Testing Account With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            account = Account()
            session.add(account)
            session.commit()


def test_account_invalid_args() -> None:
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            account = Account("email", "password") # type: ignore
            session.add(account)
            session.commit()


def test_account_valid(get_users: UserProfile) -> None:
    """Testing a Valid Account Constructor, with Required Arguments."""

    for user in get_users:
        with Session(ENGINE) as session:
            account = Account()
            account.user_id = user.id
            session.add(account)
            session.commit()

            assert account.id is not None
            assert account.status == Status.NEW
            assert isinstance(account.to_dict(), dict)

            run_test_teardown([account], session)
