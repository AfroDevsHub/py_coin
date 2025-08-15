"""Serialiser: Base Serialiser for model Model."""

from enum import Enum, EnumMeta
from json import dumps
from typing import Any, Tuple, Union

from lib.interfaces.exceptions import ApplicationError
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


class BaseSerialiser:
    """A Base/Abstract Serialiser."""

    __table__ = None
    __SERIALISER_EXCEPTION__: type[BaseException] = ApplicationError
    __VALIDATORS__ = {
        # User Profile
        "status": validate_status,
        "first_name": validate_first_name,
        "last_name": validate_last_name,
        "username": validate_username,
        "date_of_birth": validate_date_of_birth,
        "mobile_number": validate_mobile_number,
        "biography": validate_biography,
        "interests": validate_interests,
        "social_media_links": validate_social_media_links,
        # User model
        "name": validate_name,
        "description": validate_description,
        "balance": validate_balance,
        "pin": validate_pin,
        # Settings
        "data_sharing_preferences": validate_data_sharing_preferences,
        "profile_visibility_preference": validate_profile_visibility_preference,
        # Transactions
        "title": validate_username,
        # Transactions
        "amount": validate_transaction_amount,
        "transaction_status": validate_transaction_status,
        "contract_status": validate_contract_status,
        "block_type": validate_block_type,
        "previous_block_id": validate_block_previous,
        "next_block_id": validate_block_next,
    }

    def __str__(self) -> str:
        """String Representation of the Base Serialiser."""

        return "Abstract/Base Serialiser."

    def __repr__(self) -> str:
        """String Representation of the Base Serialiser."""

        return f"Application Model: {self.__class__.__name__}"

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
