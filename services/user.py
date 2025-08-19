"""User: User Services."""

from typing import Any, cast
from uuid import UUID

from pydantic import BaseModel, validate_call
from lib.interfaces.responses import ServiceResponse
from lib.interfaces.services import UserUpdateData
from lib.interfaces.user.payments import CreatePaymentProfileData
from lib.interfaces.user.profiles import CreateUserProfileData
from lib.interfaces.user.settings import CreateSettingsProfileData
from lib.interfaces.warehouse.cards import CreateCardData
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

    @handle_service_errors
    @validate_call
    def create_user_account(self, user_id: UUID):
        """Creates an Account for a given User."""

        account = AccountSerialiser().create(CreateAccountData(user_id=user_id))
        print(f"Account Created: {account.id} | User ID: {account.user_id}")

        profile = UserProfileSerialiser().create(
            CreateUserProfileData(account_id=cast(UUID, account.id))
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

    @validate_call
    def update_user_account(
        self,
        account_id: UUID,
        user_data: UserUpdateData,
    ):
        """Updates a User's Account."""

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
