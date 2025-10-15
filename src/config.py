"""App: Global Configurations."""

from datetime import datetime
from os import getenv
from uuid import uuid4, UUID
from cryptography.fernet import Fernet
from src.lib.utils.constants.users import DateTimeFormat
from src.lib.validators.config import (
    validate_card_length,
    validate_cvv_length,
    validate_end_date,
    validate_fernet_key,
    validate_salt_value,
    validate_session_id,
    validate_start_date,
)


class AppConfig:
    """Singleton Configuration Class."""

    __session__id__ = uuid4()
    __START_DATE__ = datetime.now()
    __end_date__ = datetime.now()
    __SALT_VALUE__ = UUID("0c923c48-aea7-48ce-a609-17fb120bf667")
    __FERNET_KEY__ = getenv("FERNET_KEY")
    __CARD_LENGTH__ = 13
    __CVV_LENGTH__ = 3
    __TCP_PORT__ = 42424
    __HTTP_PORT__ = 10443

    def __str__(self) -> str:
        """String Representation."""

        return f"Application Session: {self.__session__id__}"

    @property
    def session_id(self) -> str:
        """Getter: Session ID."""

        return str(validate_session_id(self.__session__id__))

    @property
    def start_date(self) -> str:
        """Getter: Start Datetime."""

        return validate_start_date(self.__START_DATE__).strftime(DateTimeFormat.STANDARD.value)

    @property
    def end_date(self) -> str:
        """Getter: End Datetime."""

        return validate_end_date(self.__end_date__, self.__START_DATE__).strftime(
            DateTimeFormat.STANDARD.value
        )

    @end_date.setter
    def end_date(self, value: datetime):
        """Setter: End Datetime."""

        self.__end_date__ = validate_end_date(value, self.__START_DATE__)

    @property
    def salt_value(self) -> UUID:
        """Getter: Salt Value."""

        return validate_salt_value(self.__SALT_VALUE__)

    @property
    def card_length(self) -> int:
        """Getter: Card Length."""

        return validate_card_length(self.__CARD_LENGTH__)

    @property
    def cvv_length(self) -> int:
        """Getter: CVV Length."""

        return validate_cvv_length(self.__CVV_LENGTH__)

    @property
    def fernet(self) -> Fernet:
        """Getter: Fernet Key."""

        return Fernet(validate_fernet_key(str(self.__FERNET_KEY__)))
