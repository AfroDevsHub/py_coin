"""User: User Services."""

from typing import Any, cast
from uuid import UUID
<<<<<<< HEAD
from lib.decorators.utils import validate_function_signature
from lib.responses import ServiceResponse
from lib.types.user import UserData
=======

from pydantic import BaseModel, validate_call
from lib.interfaces.responses import ServiceResponse
from lib.interfaces.services import UserUpdateData
from lib.interfaces.user.payments import CreatePaymentProfileData
from lib.interfaces.user.profiles import CreateUserProfileData
from lib.interfaces.user.settings import CreateSettingsProfileData
from lib.interfaces.warehouse.cards import CreateCardData
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from lib.utils.constants.responses import ServiceStatus
from lib.utils.constants.users import CardType
from serialisers.user.accounts import AccountSerialiser, CreateAccountData
from serialisers.user.payments import PaymentProfileSerialiser
from serialisers.user.profiles import UserProfileSerialiser
from serialisers.user.settings import SettingsProfileSerialiser
from serialisers.warehouse.cards import CardSerialiser
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

<<<<<<< HEAD
    @classmethod
    def create_user_account(cls, user_id: UUID, user_data: UserData):
=======
    @handle_service_errors
    @validate_call
    def create_user_account(self, user_id: UUID):
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
        """Creates an Account for a given User."""

        account = AccountSerialiser().create(CreateAccountData(user_id=user_id))
        print(f"Account Created: {account.id} | User ID: {account.user_id}")

<<<<<<< HEAD
        response = UserProfileSerialiser().create_user_profile(account["id"])
        profile_id = cls.get_public_id(response)
        profile = UserProfileSerialiser().get_user_profile(profile_id)

        response = SettingsProfileSerialiser().create_settings_profile(account["id"])
        settings_id = cls.get_public_id(response)
        settings = SettingsProfileSerialiser().get_settings_profile(settings_id)

        updated_data = cls.update_user_account(
            user_data, account["id"], profile["id"], settings["id"]
=======
        profile = UserProfileSerialiser().create(
            CreateUserProfileData(account_id=cast(UUID, account.id))
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
        )
        print(f"Profile Created: {profile.id} | User ID: {profile.account_id}")

        settings = SettingsProfileSerialiser().create(
            CreateSettingsProfileData(account_id=cast(UUID, account.id))
        )
        print(f"Settings Created: {settings.id} | User ID: {settings.account_id}")

        return ServiceResponse(
            message="User Account Successfully Created.",
            status=ServiceStatus.SUCCESS,
            data={"account": account, "profile": profile, "settings": settings},
        )

<<<<<<< HEAD
    @classmethod
=======
    @validate_call
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
    def update_user_account(
        self,
        account_id: UUID,
        user_data: UserUpdateData,
    ):
        """Updates a User's Account."""

<<<<<<< HEAD
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
=======
        account = AccountSerialiser().read(account_id)

        if user_data.account:
            AccountSerialiser().update(cast(UUID, account.id), user_data.account)
        if user_data.profile:
            UserProfileSerialiser().update(account.user_profiles.id, user_data.profile)
        if user_data.settings:
            SettingsProfileSerialiser().update(
                account.settings_profile.id, user_data.settings
            )
        if user_data.payments and account.payment_profiles:
            PaymentProfileSerialiser().update(
                account.payment_profiles.id, user_data.payments
            )
        return ServiceResponse(
            message="User Account Successfully Updated.",
            status=ServiceStatus.SUCCESS,
            data={
                "account": user_data.account,
                "profile": user_data.profile,
                "settings": user_data.settings,
            },
        )

    @handle_service_errors
    @validate_call
    def get_user_account(self, account_id: UUID) -> ServiceResponse:
        """Finds a Valid User Profile."""
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9

        account = AccountSerialiser().read(account_id)
        return ServiceResponse(
            message="User Profile Successfully Retrieved.",
            status=ServiceStatus.SUCCESS,
            data={"account": account},
        )

    @handle_service_errors
    @validate_call
    def get_user_accounts(self, user_id: UUID) -> ServiceResponse:
        """Finds a Valid User Account."""

        accounts = AccountSerialiser().get_accounts_by_user_id(user_id)
        return ServiceResponse(
            message="User Accounts Successfully Retrieved.",
            status=ServiceStatus.SUCCESS,
            data={"accounts": accounts},
        )

    @handle_service_errors
    @validate_call
    def create_payment_profile(
        self, account_id: UUID, card_type: CardType, pin: str
    ) -> ServiceResponse:
        """Creates a Payment Profile for a given Account."""

        card = CardSerialiser().create(CreateCardData(card_type=card_type, pin=pin))
        print(f"Card Created: {card.id} | Card Type: {card.card_type}")
        payment = PaymentProfileSerialiser().create(
            CreatePaymentProfileData(account_id=account_id, card_id=cast(UUID, card.id))
        )
        print(
            f"Payment Profile Created: {payment.id} | Account ID: {payment.account_id} | Card ID: {card.id}"
        )

        return ServiceResponse(
            message="Payment Profile Successfully Created.",
            status=ServiceStatus.SUCCESS,
            data={"payment": payment},
        )
