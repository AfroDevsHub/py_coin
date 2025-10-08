"""Serialiser: Base Serialiser for model Model."""

<<<<<<< HEAD
from enum import Enum, EnumMeta, EnumType
from json import dumps
from typing import Any, Tuple, Union

from lib.exceptions import ApplicationError
from lib.utils.encryption.cryptography import encrypt_data
from lib.validators.blocks import (
    validate_block_next,
    validate_block_previous,
    validate_block_type,
)
from lib.validators.contracts import validate_contract_status
from lib.validators.transactions import (
    validate_transaction_amount,
    validate_transaction_status,
)
from lib.validators.users import (
    validate_balance,
    validate_biography,
    validate_data_sharing_preferences,
    validate_date_of_birth,
    validate_description,
    validate_first_name,
    validate_interests,
    validate_last_name,
    validate_mobile_number,
    validate_name,
    validate_pin,
    validate_profile_visibility_preference,
    validate_social_media_links,
    validate_status,
    validate_username,
)
from models.model import BaseModel
=======
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from sqlalchemy.orm.decl_api import DeclarativeMeta
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9

class ISerialiser(ABC):
    """A Base/Abstract Serialiser."""

    @abstractmethod
    def create(self, data: Any) -> DeclarativeMeta:
        pass

    @abstractmethod
    def read(self, model_id: UUID) -> DeclarativeMeta:
        pass

    @abstractmethod
    def update(self, model_id: UUID, data: Any) -> DeclarativeMeta:
        pass

<<<<<<< HEAD
    def __repr__(self) -> str:
        """String Representation of the Base Serialiser."""

        return f"Application Model: {self.__class__.__name__}"

    def validate_serialiser_kwargs(self, key: str, value: Any, model=None) -> Any:
        """Updates Validated Model Attributes."""

        data_type, nullable, validator = self.__get_column_data__(key)

        if not nullable and value is None:
            raise self.__SERIALISER_EXCEPTION__("Non-Nullable Attribute.")

        if (
            isinstance(data_type, EnumType)
            and hasattr(data_type, "__dict__")
            and isinstance(data_type.__dict__, dict)
            and value in data_type.__dict__.get("_value2member_map_", {})
        ):
            return data_type.__dict__["_value2member_map_"][value]

        if not isinstance(value, data_type) and value is not None:

            raise self.__SERIALISER_EXCEPTION__(
                f"Invalid Type for this Attribute. Expected {data_type} but got {value}"
            )

        if validator is not None and hasattr(validator, "__call__"):
            value = validator(value, model=model)

        return value

    def __get_column_data__(
        self, key: str
    ) -> Tuple[EnumMeta, bool, Union["function", None]]:
        """Extract a Columns Meta-Data."""

        if self.__table__ is None:
            raise self.__SERIALISER_EXCEPTION__("Invalid Table Meta Data")

        column = dict(self.__table__.columns).get(key)
        return (
            column.type.python_type,
            column.nullable,
            self.__VALIDATORS__.get(column.name),
        )

    @classmethod
    def __get_encrypted_model_data__(cls, model: BaseModel) -> str:
        """Get model Information."""

        data = model.to_dict()
        if hasattr(model, "login_history"):
            data.update(
                {
                    "login_history": [
                        cls.__get_encrypted_model_data__(login_history)
                        for login_history in model.login_history
                        if login_history.logged_in
                    ]
                }
            )

        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value
        return encrypt_data(dumps(data).encode())

    @classmethod
    def __get_model_data__(cls, model: BaseModel) -> dict[str, Any]:
        """Gets the Model Data."""

        data = model.to_dict()
        if hasattr(model, "user_profiles"):
            data.update(
                {
                    "user_profiles": [
                        profile.to_dict() for profile in model.user_profiles
                    ]
                }
            )

        if hasattr(model, "payment_profiles"):
            data.update(
                {
                    "payment_profiles": [
                        payment.to_dict() for payment in model.payment_profiles
                    ]
                }
            )

        if hasattr(model, "settings_profile"):
            data.update(
                {
                    "settings_profile": [
                        settings.to_dict() for settings in model.settings_profile
                    ]
                }
            )
        return data
=======
    @abstractmethod
    def delete(self, model_id: UUID) -> str:
        pass
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
