"""Encryption: Testing Encoders Module."""

from typing import Any
from uuid import uuid4
from pytest import mark, raises
from lib.utils.encryption.encoders import get_hash_value


@mark.parametrize(
    "data",
    [
        ("Testing Hash Value.", ""),
        (str(uuid4()), str(uuid4())),
        (str(123456789), str(123456789)),
    ],
)
def test_get_hash_value(data: Any) -> None:
    """Test Valid Hash Value."""

    assert len(get_hash_value(data[0])) == 64
    assert get_hash_value(data[0]) is not None
    assert isinstance(get_hash_value(data[0], data[1]), str)


@mark.parametrize(
    "data",
    [
        ("Testing Hash Value.", None),
        (str(uuid4()), 1),
        (str(123456789), uuid4()),
    ],
)
def test_get_hash_value_invalid_salt(data: Any) -> None:
    """Test Invalid Salt Value."""

    with raises(ValueError, match="Salt must be a String."):
        get_hash_value(data[0], data[1])


@mark.parametrize(
    "data",
    [
        (123456789, ""),
        (uuid4(), str(uuid4())),
        (None, 123456789),
    ],
)
def test_get_hash_value_invalid_value(data: Any) -> None:
    """Test Invalid Hash Value."""

    with raises(ValueError, match="Value must be a String."):
        get_hash_value(data[0], data[1])
