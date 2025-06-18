"""User: User Services."""

from typing import Optional
from uuid import UUID
from lib.decorators.utils import validate_function_signature
from lib.responses import ServiceResponse
from lib.types.user import UserData
from lib.utils.constants.responses import ServiceStatus
from serialisers.user.accounts import AccountSerialiser
from serialisers.user.profiles import UserProfileSerialiser
from serialisers.user.settings import SettingsProfileSerialiser
from services.abstract import AbstractService


class UserService(AbstractService):
    """Manages User Operations."""

    __instance__ = None

    def __new__(cls, *args, **kwargs) -> "UserService":
        """Singleton Class Constructor."""

        if not cls.__instance__:
            return super().__new__(cls, *args, **kwargs)
        return cls.__instance__

    @classmethod
    def create_user_account(cls, user_id: UUID, user_data: UserData):
        """Creates an Account for a given User."""

        response = AccountSerialiser().create_account(user_id)
        account_id = cls.get_public_id(response)
        account = AccountSerialiser().get_account(account_id)

        response = UserProfileSerialiser().create_user_profile(account["id"])
        profile_id = cls.get_public_id(response)
        profile = UserProfileSerialiser().get_user_profile(profile_id)

        response = SettingsProfileSerialiser().create_settings_profile(account["id"])
        settings_id = cls.get_public_id(response)
        settings = SettingsProfileSerialiser().get_settings_profile(settings_id)

        updated_data = cls.update_user_account(
            user_data, account["id"], profile["id"], settings["id"]
        )
        account = cls.get_user_account(account["account_id"])
        return ServiceResponse(
            "User Account Successfully Created.",
            ServiceStatus.SUCCESS,
            {"account": account.data, "updated": updated_data},
        )

    @classmethod
    def update_user_account(
        cls,
        user_data: UserData,
        account_id: Optional[str],
        profile_id: Optional[str],
        settings_id: Optional[str],
    ):
        """Updates a User's Account."""

        if account_id:
            AccountSerialiser().update_account(account_id, **user_data.get("account"))
        if profile_id:
            UserProfileSerialiser().update_user_profile(
                profile_id, **user_data.get("profile")
            )
        if settings_id:
            SettingsProfileSerialiser().update_settings_profile(
                settings_id, **user_data.get("settings")
            )
        return ServiceResponse(
            "User Account Successfully Updated.",
            ServiceStatus.SUCCESS,
            {
                "account": user_data.get("account"),
                "profile": user_data.get("profile"),
                "settings": user_data.get("settings"),
            },
        )

    @classmethod
    def get_user_account(cls, account_id: str) -> ServiceResponse:
        """Finds a Valid User Account."""

        account = AccountSerialiser().get_account(account_id)
        return ServiceResponse(
            "User Account Successfully Retrieved.", ServiceStatus.SUCCESS, account
        )

    # def add_payment_profile():
    #     pass

    # def remove_payment_profile():
    #     pass
