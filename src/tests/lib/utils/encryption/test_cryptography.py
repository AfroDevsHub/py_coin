"""Encryption: Testing Cryptography Module."""

from typing import Any
from uuid import uuid4
from pytest import mark, raises
from config import AppConfig
from lib.exceptions import UserError
from lib.utils.encryption.cryptography import encrypt_data, decrypt_data


@mark.parametrize(
    "data",
    [
        "Testing Hash Value.",
        str(uuid4()),
        str(123456789),
    ],
)
def test_encrypt_data(data: Any) -> None:
    """Test Encrypted Data."""

    assert encrypt_data(data.encode()) is not None
    assert encrypt_data(data.encode()) != data
    assert len(encrypt_data(data.encode())) >= 100


@mark.parametrize(
    "data",
    [
        None,
        uuid4(),
        123456789,
    ],
)
def test_invalid_encrypt_data(data: Any) -> None:
    """Test Encrypted Data."""

    with raises((UserError, AttributeError)):
        encrypt_data(data.encode())


@mark.parametrize(
    "data",
    [
        "Testing Hash Value.",
        str(uuid4()),
        str(123456789),
    ],
)
def test_decrypt_data(data: Any) -> None:
    """Test Decrypted Data."""

    fernet = AppConfig().fernet
    encrypted_data = fernet.encrypt(data.encode()).decode()
    assert decrypt_data(encrypted_data) is not None
    assert decrypt_data(encrypted_data) != encrypted_data
    assert decrypt_data(encrypted_data) == data


@mark.parametrize(
    "data",
    [
        None,
        uuid4(),
        123456789,
    ],
)
def test_invalid_decrypt_data(data: Any) -> None:
    """Test Decrypted Data."""

    with raises((UserError, AttributeError)):
        fernet = AppConfig().fernet
        encrypted_data = fernet.encrypt(data.encode()).decode()
        decrypt_data(encrypted_data)
