"""Encryption: Contains Encoders (SHA256)."""

from hashlib import sha256


def get_hash_value(value: str, salt_value: str = "") -> str:
    """Generates a new Hash Value."""

    if not isinstance(value, str):
        raise ValueError("Value must be a String.")

    if not isinstance(salt_value, str):
        raise ValueError("Salt must be a String.")

    sha256_value = sha256(salt_value.encode("utf-8"))
    sha256_value.update(value.encode("utf-8"))
    return sha256_value.hexdigest()
