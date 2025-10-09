"""Encryption: Contains Data Encrypters."""

from cryptography.fernet import Fernet
from config import AppConfig
from lib.exceptions import UserError


def encrypt_data(data: bytes) -> str:
    """Returns Encrypted Data."""

    fernet = AppConfig().fernet
    if not isinstance(fernet, Fernet):
        raise UserError("Invalid User Data")
    return fernet.encrypt(data).decode()


def decrypt_data(data: str) -> str:
    """Returns Decrypted Data."""

    fernet = AppConfig().fernet
    if not isinstance(fernet, Fernet):
        raise UserError("Invalid User Data")
    return fernet.decrypt(data.encode()).decode()
