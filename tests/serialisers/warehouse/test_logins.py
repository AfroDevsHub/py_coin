"""Warehouse: Testing User Serialiser."""

from datetime import datetime
from uuid import uuid4

from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from lib.exceptions import LoginHistoryError
from lib.utils.constants.users import Country, LoginMethod
from models.warehouse.logins import LoginHistory
from serialisers.warehouse.logins import LoginHistorySerialiser
from models import ENGINE
from services.authentication import AbstractService
from conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


def test_loginhistoryserialiser_create(get_users):
    """Testing User Serialiser: Create User."""

    for user in get_users:
        with Session(ENGINE) as session:
            login_history = LoginHistorySerialiser().create_login_history(user.id)
            login_id = AbstractService.get_public_id(login_history)
            login = (
                session.query(LoginHistory)
                .filter(LoginHistory.login_id == login_id)
                .one_or_none()
            )
            assert login.id is not None
            run_test_teardown([login], session)


@mark.parametrize("data", check_invalid_ids())
def test_loginhistoryserialiser_create_invalid(data):
    """Testing User Serialiser: Invalid Create User [Email]."""

    with raises((LoginHistoryError, DataError, ProgrammingError)):
        LoginHistorySerialiser().create_login_history(data)


def test_loginhistoryserialiser_get(get_logins):
    """Testing User Serialiser: Get User."""

    for login in get_logins:
        login_history = LoginHistorySerialiser().get_login_history(login.login_id)

        assert isinstance(login_history, dict)
        for key in login_history:
            assert key not in LoginHistory.__EXCLUDE_ATTRIBUTES__


@mark.parametrize("data", check_invalid_ids())
def test_loginhistoryserialiser_get_invalid(data):
    """Testing User Serialiser: Invalid Get User."""

    with raises((LoginHistoryError, DataError, ProgrammingError)):
        LoginHistorySerialiser().get_login_history(data)


def test_loginhistoryserialiser_delete(get_logins):
    """Testing User Serialiser: Invalid Get User."""

    for logins in get_logins:
        assert (
            LoginHistorySerialiser()
            .delete_login_history(logins.id)
            .startswith("Deleted: ")
        )


@mark.parametrize("data", check_invalid_ids())
def test_loginhistoryserialiser_delete_invalid(data):
    """Testing User Serialiser: Invalid Delete User."""

    with raises((LoginHistoryError, DataError, ProgrammingError)):
        LoginHistorySerialiser().delete_login_history(data)


@mark.parametrize(
    "data",
    [
        {
            "session_id": uuid4(),
            "login_location": Country.ALBANIA,
            "login_device": "Chrome",
            "login_method": LoginMethod.EMAIL,
            "logged_in": True,
            "logout_date": datetime.now(),
            "authentication_token": str(uuid4()),
        },
    ],
)
def test_loginhistoryserialiser_update_valid(get_logins, data):
    """Testing User Serialiser: Update User."""

    for login in get_logins:
        with Session(ENGINE) as session:
            LoginHistorySerialiser().update_login_history(
                login.id,
                **data,
            )
            login = session.get(LoginHistory, login.id)

            for key, value in data.items():
                assert getattr(login, key) == value


@mark.parametrize(
    "data",
    [
        {
            "session_id": None,
            "login_location": None,
            "login_device": None,
            "login_method": None,
            "logged_in": None,
            "logout_date": None,
            "authentication_token": None,
        },
        {
            "session_id": "Non UUID",
            "login_location": 1234,
            "login_device": 1234,
            "login_method": 1234,
            "logged_in": 12255,
            "logout_date": 23455,
            "authentication_token": 57980,
        },
    ],
)
def test_loginhistoryserialiser_update_invalid(get_logins, data):
    """Testing User Serialiser: Invalid Update User [PASSWORD]."""

    for login in get_logins:
        with raises((LoginHistoryError, DataError, ProgrammingError)):
            LoginHistorySerialiser().update_login_history("login.id", **data)
