"""Validators: Testing Application Config Module."""

from datetime import date, datetime, timedelta
from typing import Any
from uuid import uuid4

from pytest import mark, raises

from src.lib.types.exceptions import ApplicationError
from lib.validators.config import (
    validate_cvv_length,
    validate_end_date,
    validate_salt_value,
    validate_fernet_key,
    validate_session_id,
    validate_card_length,
    validate_start_date,
)


@mark.parametrize(
    "data",
    [uuid4(), uuid4()],
)
def test_validate_salt_value(data: Any) -> None:
    """Tests Validating Salt Value."""

    assert validate_salt_value(data)


@mark.parametrize(
    "data",
    [1, None, validate_card_length],
)
def test_invalidate_salt_value(data: Any) -> None:
    """Tests Invalidates Salt Value."""

    with raises(ApplicationError):
        validate_salt_value(data)


@mark.parametrize(
    "data",
    ["fernet-key", "Any Valid String."],
)
def test_validate_fernet_key(data: Any) -> None:
    """Tests Validating Fernet Key."""

    assert validate_fernet_key(data) == data


@mark.parametrize(
    "data",
    [1, None, validate_card_length],
)
def test_invalidate_fernet_key(data: Any) -> None:
    """Tests Invalidates Fernet Key."""

    with raises(ApplicationError):
        validate_fernet_key(data)


@mark.parametrize(
    "data",
    [datetime.now(), datetime(2010, 12, 31, 15, 1, 15), datetime(1972, 1, 15, 0, 0, 0)],
)
def test_validate_start_date(data: Any) -> None:
    """Tests Validating Start Date."""

    assert validate_start_date(data) == data


@mark.parametrize(
    "data",
    ["2022-05-20", date(2010, 12, 31), date(1972, 1, 15), 20220519],
)
def test_invalidate_start_date(data: Any) -> None:
    """Tests Invalidates Start Date."""

    with raises(ApplicationError):
        validate_start_date(data)


@mark.parametrize(
    "data",
    [
        (datetime.now(), datetime.now() - timedelta(days=1)),
        (
            datetime(2010, 12, 31, 15, 1, 15),
            datetime(2010, 12, 31, 15, 1, 15) - timedelta(hours=1),
        ),
        (
            datetime(1972, 1, 15, 0, 0, 0),
            datetime(1972, 1, 15, 0, 0, 0) - timedelta(seconds=1),
        ),
    ],
)
def test_validate_end_date(data: Any) -> None:
    """Tests Validating End Date."""

    assert validate_end_date(data[0], data[1]) == data[0]


@mark.parametrize(
    "data",
    [
        ("2022-05-20", "2021-04-15"),
        (
            datetime(1972, 1, 15, 0, 0, 0),
            datetime(1972, 1, 15, 0, 0, 0),
        ),
        (
            datetime(1972, 1, 15, 0, 0, 0),
            datetime(1972, 1, 15, 0, 0, 0) + timedelta(seconds=1),
        ),
        (date(2010, 12, 31), date(2008, 12, 31)),
        (date(1972, 1, 15), date(2010, 12, 31)),
        (20220519, 20100515),
    ],
)
def test_invalidate_end_date(data: Any) -> None:
    """Tests Invalidates End Date."""

    with raises(ApplicationError):
        validate_end_date(data[0], data[1])


@mark.parametrize(
    "data",
    [9, 15, 27],
)
def test_validate_card_length(data: Any) -> None:
    """Tests Validating Card length."""

    assert validate_card_length(data) == data


@mark.parametrize(
    "data",
    [-9, 0, "27", 27.0, 0.0],
)
def test_invalidate_card_length(data: Any) -> None:
    """Tests Validating Card length."""

    with raises(ApplicationError):
        validate_card_length(data)


@mark.parametrize(
    "data",
    [3, 19, 115, 270],
)
def test_validate_cvv_length(data: Any) -> None:
    """Tests Validating CVV Length."""

    assert validate_cvv_length(data) == data


@mark.parametrize(
    "data",
    [-9, 0, "27", 27.0, 0.0],
)
def test_invalidate_cvv_length(data: Any) -> None:
    """Tests Invalidates CVV Length."""

    with raises(ApplicationError):
        validate_cvv_length(data)


@mark.parametrize(
    "data",
    [uuid4(), uuid4()],
)
def test_validate_session_id(data: Any) -> None:
    """Tests Validating Session ID."""

    assert validate_session_id(data) == data


@mark.parametrize(
    "data",
    [1, None, validate_card_length, "uuid value as a string"],
)
def test_invalidate_session_id(data: Any) -> None:
    """Tests Invalidates Session ID."""

    with raises(ApplicationError):
        validate_session_id(data)
