"""User: User Services."""

from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, validate_call
from lib.interfaces.responses import ServiceResponse
from lib.interfaces.data_classes import UserData
from lib.utils.constants.responses import ServiceStatus
from lib.utils.helpers.users import get_public_uuid
from serialisers.user.accounts import AccountSerialiser
from serialisers.user.profiles import UserProfileSerialiser
from serialisers.user.settings import SettingsProfileSerialiser
from services.authentication import handle_service_errors


class UserAccountData(BaseModel):
    """Data Model for User Account."""

    account: dict[str, Any] | None = None
    profile: dict[str, Any] | None = None
    settings: dict[str, Any] | None = None

class UserService:
    """Manages User Operations."""

    __instance__ = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "UserService":
        """Singleton Class Constructor."""

        if not cls.__instance__:
            return super().__new__(cls, *args, **kwargs)
        return cls.__instance__

    @handle_service_errors
    @validate_call
    def create_user_account(cls, user_id: str):
        """Creates an Account for a given User."""

        response = AccountSerialiser().create_account(user_id)
        account_id = get_public_uuid(response)
        account = AccountSerialiser().get_account(account_id)

        response = UserProfileSerialiser().create_user_profile(account["id"])
        
        response = SettingsProfileSerialiser().create_settings_profile(account["id"])
        
        return ServiceResponse(
            message="User Account Successfully Created.",
            status=ServiceStatus.SUCCESS,
            data={"account": account},
        )

    # @classmethod
    # @validate_call
    # def update_user_account(
    #     cls,
    #     user_data: UserData,
    #     account_id: Optional[str],
    #     profile_id: Optional[str],
    #     settings_id: Optional[str],
    # ):
    #     """Updates a User's Account."""

    #     if account_id:
    #         AccountSerialiser().update_account(
    #             account_id, **user_data.account.to_dict()
    #         )
    #     if profile_id:
    #         UserProfileSerialiser().update_user_profile(
    #             profile_id, **user_data.profile.to_dict()
    #         )
    #     if settings_id:
    #         SettingsProfileSerialiser().update_settings_profile(
    #             settings_id, **user_data.settings.to_dict()
    #         )
    #     return ServiceResponse(
    #         "User Account Successfully Updated.",
    #         ServiceStatus.SUCCESS,
    #         {
    #             "account": user_data.account.to_dict(),
    #             "profile": user_data.profile.to_dict(),
    #             "settings": user_data.settings.to_dict(),
    #         },
    #     )

    # @classmethod
    # @validate_call
    # def get_user_account(cls, account_id: str) -> ServiceResponse:
    #     """Finds a Valid User Account."""

    #     account = AccountSerialiser().get_account(account_id)
    #     return ServiceResponse(
    #         "User Account Successfully Retrieved.", ServiceStatus.SUCCESS, account
    #     )