"""Users: Testing User Model."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import ENGINE
from models.user.users import User
from lib.utils.constants.users import Role, Status
from conftest import run_test_teardown


def test_user_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            user = User()
            session.add(user)
            session.commit()


def test_user_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            user = User("email", "password")
            session.add(user)
            session.commit()


def test_user_valid():
    """Testing a Valid User Constructor, with Required Arguments."""

    with Session(ENGINE) as session:
        user = User()
        user.email = "test3@test.com"
        user.password = "password123@"
        user.user_id = "test_user_id"

        session.add(user)
        session.commit()

        assert user.id is not None
        assert user.status == Status.NEW
        assert user.role == Role.USER
        assert isinstance(user.to_dict(), dict)

        run_test_teardown([user], session)
