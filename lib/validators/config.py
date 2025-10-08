"""Config: validations for Application Config related Models."""

from datetime import datetime
from uuid import UUID

from lib.exceptions import ApplicationError


def validate_salt_value(salt_value: UUID) -> UUID:
    """Validates Salt Value."""

    if not isinstance(salt_value, UUID):
        raise ApplicationError("Invalid Type for this Attribute.")
    if not salt_value:
        raise ApplicationError("Invalid Application Configuration.")
    return salt_value


def validate_fernet_key(fernet_key: str) -> str:
    """Validates Fernet Key."""

    if not isinstance(fernet_key, str):
        raise ApplicationError("Invalid Type for this Attribute.")
    if not fernet_key:
        raise ApplicationError("Invalid Application Configuration.")
    return fernet_key


def validate_start_date(start_date: datetime) -> datetime:
    """Validates Start Date."""

    if not isinstance(start_date, datetime):
        raise ApplicationError("Invalid Type for this Attribute.")
    return start_date


def validate_end_date(end_date: datetime, start_date: datetime) -> datetime:
    """Validates End Date."""

    if not isinstance(end_date, datetime):
        raise ApplicationError("Invalid Type for this Attribute. [End Date]")
    if not isinstance(start_date, datetime):
        raise ApplicationError("Invalid Type for this Attribute. [Start Date]")
    if end_date <= start_date:
        raise ApplicationError("Invalid Application Configuration.")
    return end_date


def validate_card_length(card_length: int) -> int:
    """Validates Card length."""

    if not isinstance(card_length, int):
        raise ApplicationError("Invalid Type for this Attribute.")
    if card_length <= 0:
        raise ApplicationError("Invalid Application Configuration.")
    return card_length


def validate_cvv_length(cvv_number: int) -> int:
    """Validates CVV Length."""

    if not isinstance(cvv_number, int):
        raise ApplicationError("Invalid Type for this Attribute.")
    if cvv_number <= 0:
        raise ApplicationError("Invalid Application Configuration.")
    return cvv_number


def validate_session_id(session_id: UUID) -> UUID:
    """Validates Session ID."""

    if not isinstance(session_id, UUID):
        raise ApplicationError("Invalid Application Configuration.")
    return session_id
