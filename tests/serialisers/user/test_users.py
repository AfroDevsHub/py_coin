"""User: Testing User Serialiser."""

import json
from uuid import uuid4

from pydantic import ValidationError
from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError, DataError

from config import AppConfig
from lib.exceptions import UserError
from lib.types.user import UserUpdateData
from lib.utils.constants.users import Status
from lib.utils.encryption.encoders import get_hash_value
from serialisers.user.users import UserSerialiser
from models import ENGINE
from models.user.users import User
from services.authentication import AbstractService
from conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


@mark.parametrize(
    "data",
    [
        ("test@test.com", "password@test1"),
        ("newemail@email.co.za", "password123-_"),
        ("newapp@app.co.org", "password_test1"),
    ],
)
def test_userserialiser_create(data):
    """Testing User Serialiser: Create User."""

    with Session(ENGINE) as session:
        user = UserSerialiser().create_user(data[0], data[1])
        user_id = AbstractService.get_public_id(user)

        user = session.query(User).filter(User.user_id == user_id).one_or_none()
        assert user.id is not None
        assert user.status == Status.NEW
        run_test_teardown([user], session)


@mark.parametrize(
    "data",
    [
        (None, "password@test1"),
        ("newemail#email.co.za", "password123-_"),
        ("newapp@app.c", "password_test1"),
        ("newapp@app.co.g", "password_test1"),
        ("newapp@app.", "password_test1"),
        (1, "password_test1"),
        ("test@test.com", None),
        ("test@test.com", "password"),
        ("newemail@email.co.za", "p123"),
        ("newapp@app.co.org", "p"),
        ("newapp@app.co.org", 1),
    ],
)
def test_userserialiser_create_invalid(data):
    """Testing User Serialiser: Invalid Create User [Email]."""

    with raises(UserError):
        UserSerialiser().create_user(data[0], data[1])


def test_userserialiser_get(get_users):
    """Testing User Serialiser: Get User."""

    for user in get_users:
        user = UserSerialiser().get_user(user.user_id)
        user_data = json.loads(AppConfig().fernet.decrypt(user.encode()).decode())

        assert isinstance(user_data, dict)
        for key in user_data:
            assert key not in User.__EXCLUDE_ATTRIBUTES__


@mark.parametrize("data", check_invalid_ids())
def test_userserialiser_get_invalid(data):
    """Testing User Serialiser: Invalid Get User."""

    with raises((UserError, ProgrammingError)):
        UserSerialiser().get_user(data)


def test_userserialiser_delete(get_users):
    """Testing User Serialiser: Delete User."""

    for user in get_users:
        assert UserSerialiser().delete_user(user.id).startswith("Deleted: ")


@mark.parametrize("data", check_invalid_ids())
def test_userserialiser_delete_invalid(data):
    """Testing User Serialiser: Invalid Delete User."""

    with raises((UserError, DataError, ProgrammingError)):
        UserSerialiser().delete_user(data)


@mark.parametrize(
    "data",
    [
        ("password123@1", Status.ACTIVE),
        ("password123@2", Status.DELETED),
        ("password123@3", Status.NEW),
    ],
)
def test_userserialiser_update_valid(get_users, data):
    """Testing User Serialiser: Update User [PASSWORD]."""

    for user in get_users:
        with Session(ENGINE) as session:
            UserSerialiser().update_user(user.id, UserUpdateData(password=data[0], status=data[1]))
            user = session.get(User, user.id)

            assert user.id is not None
            assert user.password == str(get_hash_value(data[0], str(user.salt_value)))
            assert user.status == data[1]


@mark.parametrize(
    "data",
    [
        ("password123@1", Status.DISABLED),
        ("password123@1", "Any String."),
        ("password123@3", 1),
        ("password123@3", None),
        (None, Status.ACTIVE),
        ("@pass", Status.ACTIVE),
        (1, Status.ACTIVE),
        (Status.ACTIVE, Status.ACTIVE),
        ("Status.ACTIVE", Status.ACTIVE),
        None,
        "User ID",
        1,
        uuid4(),
        (None, Status.ACTIVE),
        ("password123@2", None),
    ],
)
def test_userserialiser_update_invalid(get_users, data):
    """Testing User Serialiser: Invalid Update User [PASSWORD]."""

    for user in get_users:
        with raises((UserError, DataError, TypeError, ValidationError)):
            UserSerialiser().update_user(user.id, UserUpdateData(password=data[0], status=data[1]))
            if not isinstance(data, list):
                UserSerialiser().update_user("Invalid User ID")
