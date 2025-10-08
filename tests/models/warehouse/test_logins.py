"""Warehouse: Testing Login History Model."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import ENGINE
from models.warehouse.logins import LoginHistory
from conftest import run_test_teardown


def test_login_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            login_history = LoginHistory()
            session.add(login_history)
            session.commit()


def test_login_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            login_history = LoginHistory("email", "password")
            session.add(login_history)
            session.commit()


def test_login_valid(get_users):
    """Testing a Valid LoginHistory Constructor, with Required Arguments."""

    for user in get_users:
        with Session(ENGINE) as session:
            login_history = LoginHistory()
            login_history.user_id = user.id
            session.add(login_history)
            session.commit()

            assert login_history.id is not None
            assert login_history.logged_in

            run_test_teardown([login_history], session)
