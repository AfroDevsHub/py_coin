"""Tests: Testing Application Config Module."""

from datetime import datetime, timedelta

from pytest import raises
from config import AppConfig
from lib.utils.constants.users import DateTimeFormat


def test_app_config_str_repr():
    """Test AppConfig Init - Class Representaion."""

    assert str(AppConfig()).startswith("Application Session: ")


def test_app_config_session_id():
    """Test AppConfig Init - Session ID."""

    assert AppConfig().session_id is not None


def test_app_config_start_date():
    """Test AppConfig Init - Start Date."""

    assert str(AppConfig().start_date) <= (
        (datetime.now() + timedelta(seconds=8)).strftime(DateTimeFormat.STANDARD.value)
    ) and str(AppConfig().start_date) >= (
        datetime.now() - timedelta(seconds=8)
    ).strftime(
        DateTimeFormat.STANDARD.value
    )


def test_app_config_start_date_setter():
    """Test AppConfig Start Date Setter."""

    with raises(AttributeError):
        AppConfig().start_date = datetime.now().strftime(DateTimeFormat.STANDARD.value)


def test_app_config_end_date():
    """Test AppConfig Init - End Date."""

    assert datetime.strptime(
        str(AppConfig().end_date), DateTimeFormat.STANDARD.value
    ) >= datetime.strptime(str(AppConfig().start_date), DateTimeFormat.STANDARD.value)


def test_app_config_end_date_setter():
    """Test AppConfig End Date Setter."""

    now = datetime.now()
    setattr(AppConfig(), "end_date", now)
    assert AppConfig().end_date is not None


def test_app_config_salt_value():
    """Test AppConfig Init - Salt Value."""

    assert AppConfig().salt_value is not None


def test_app_config_salt_value_setter():
    """Test AppConfig Salt Value Setter."""

    with raises(AttributeError):
        AppConfig().salt_value = "Testing Setter"


def test_app_config_card_length():
    """Test AppConfig Init - Salt Value."""

    assert AppConfig().card_length is not None


def test_app_config_card_length_setter():
    """Test AppConfig Salt Value Setter."""

    with raises(AttributeError):
        AppConfig().card_length = 12


def test_app_config_cvv_length():
    """Test AppConfig Init - Salt Value."""

    assert AppConfig().cvv_length is not None


def test_app_config_cvv_length_setter():
    """Test AppConfig Salt Value Setter."""

    with raises(AttributeError):
        AppConfig().cvv_length = 5
