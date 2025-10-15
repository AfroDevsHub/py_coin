"""User: User Services."""

from typing import Any, cast
from uuid import UUID

from pydantic import validate_call
from src.lib.interfaces.responses import ServiceResponse
from src.lib.types.services.user import UserUpdateData
from src.lib.types.user.payments import CreatePaymentProfileData
from src.lib.types.user.profiles import CreateUserProfileData
from src.lib.types.user.settings import CreateSettingsProfileData
from src.lib.types.warehouse.cards import CreateCardData
from src.lib.utils.constants.responses import ServiceStatus
from src.lib.utils.constants.users import CardType
from src.serialisers.user.accounts import AccountSerialiser, CreateAccountData
from src.serialisers.user.payments import PaymentProfileSerialiser
from src.serialisers.user.profiles import UserProfileSerialiser
from src.serialisers.user.settings import SettingsProfileSerialiser
from src.serialisers.user.users import UserSerialiser
from src.serialisers.warehouse.cards import CardSerialiser
from src.services.authentication import handle_service_errors


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
    def validate_user(self, user_id: UUID) -> ServiceResponse:
        """Validates if a User Exists."""

        user = UserSerialiser().read(user_id)
        if not user:
            return ServiceResponse(
                message="User Does Not Exist.",
                status=ServiceStatus.ERROR,
                data={},
            )
        return ServiceResponse(
            message="User Successfully Validated.",
            status=ServiceStatus.SUCCESS,
            data={"user": user},
        )
    
    @handle_service_errors
    @validate_call
    def validate_account(self, user_id: UUID) -> ServiceResponse:
        """Validates if an Account Exists."""

        accounts = AccountSerialiser().get_accounts_by_user_id(user_id)
        if not accounts:
            return ServiceResponse(
                message="Account Does Not Exist.",
                status=ServiceStatus.ERROR,
                data={},
            )
        return ServiceResponse(
            message="Account Successfully Validated.",
            status=ServiceStatus.SUCCESS,
            data={"account": accounts},
        )

    @handle_service_errors
    @validate_call
    def create_user_account(self, user_id: UUID) -> ServiceResponse:
        """Creates an Account for a given User."""

        account = AccountSerialiser().create(CreateAccountData(user_id=user_id))
        print(f"Account Created: {account.id} | User ID: {account.user_id}")

        profile = UserProfileSerialiser().create(
            CreateUserProfileData(account_id=cast(UUID, account.id))
        )
        print(f"Profile Created: {profile.id} | Account ID: {profile.account_id}")

        settings = SettingsProfileSerialiser().create(
            CreateSettingsProfileData(account_id=cast(UUID, account.id))
        )
        print(f"Settings Created: {settings.id} | Account ID: {settings.account_id}")

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
            AccountSerialiser().update(account_id, user_data.account)
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
