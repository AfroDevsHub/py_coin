"""Test-Utils: Configure Users Module."""

from datetime import date
from uuid import UUID
from config import AppConfig
from lib.utils.constants.users import CardType, DateFormat, Status
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models.user.accounts import Account
from models.user.payments import PaymentProfile
from models.user.profiles import UserProfile
from models.user.settings import SettingsProfile
from models.user.users import User
from models.warehouse.cards import Card
from models.warehouse.logins import LoginHistory

STATUSES = [
    Status.NEW,
    Status.ACTIVE,
    Status.DELETED,
]


def create_user(email: str, password: str, status: Status) -> User:
    """Creates a test User."""

    user = User()
    user.email = encrypt_data(email.encode())
    user.password = get_hash_value(password, str(user.salt_value))
    user.user_id = get_hash_value(email + password, str(AppConfig().salt_value))
    user.status = status
    return user


def create_users() -> list[User]:
    """Creates Test Users."""

    user = create_user("testc3@test.com", "password123@", STATUSES[0])
    user1 = create_user("test13c@test.com", "password123@1", STATUSES[1])
    user2 = create_user("test23c@test.com", "password123@2", STATUSES[2])
    return [user, user1, user2]


def create_account(user_id: UUID, status: Status) -> Account:
    """Creates a Test Account."""

    account = Account()
    account.user_id = user_id
    account.status = status
    return account


def create_accounts(user_ids: list[UUID]) -> list[Account]:
    """Creates a Test Account."""

    users = []
    for user_id, status in zip(user_ids, STATUSES):
        users.append(create_account(user_id, status))
    return users


def create_setting(account_id: UUID) -> SettingsProfile:
    """Creates a Test Settings Profile."""

    setting = SettingsProfile()
    setting.account_id = account_id
    return setting


def create_settings(account_ids: list[UUID]) -> list[SettingsProfile]:
    """Creates Test Settings Profiles."""

    settings = []
    for account_id in account_ids:
        settings.append(create_setting(account_id))
    return settings


def create_card(
    card_number: str, card_type: CardType, cvv_number: str, pin: str
) -> Card:
    """Creates a Test Card."""

    card = Card()
    card.card_number = card_number
    card.card_type = card_type
    card.cvv_number = cvv_number
    card.expiration_date = date.today()
    card.pin = pin
    card.card_id = get_hash_value(
        card_number + cvv_number + date.today().strftime(DateFormat.HYPHEN.value),
        str(card.salt_value),
    )

    return card


def create_cards() -> list[Card]:
    """Creates Test Settings Profiles."""

    cards = []
    base = "12545"
    for card in CardType:
        card_type = card.value[1]
        cards.append(
            create_card(
                f"{card_type}{base}{card_type}", card, card_type[-3:], f"{card_type}99"
            )
        )
    return cards


def create_payment_profile(
    account_id: UUID, card_id: UUID, status: Status
) -> PaymentProfile:
    """Creates a Test Payment Profile."""

    payment = PaymentProfile()
    payment.account_id = account_id
    payment.card_id = card_id
    payment.status = status
    return payment


def create_payment_profiles(
    account_ids: list[UUID], card_ids: list[UUID]
) -> list[PaymentProfile]:
    """Creates Test Payment Profiles."""

    payment_profile = []
    for account_id, card_id, status in zip(account_ids, card_ids, STATUSES):
        payment_profile.append(create_payment_profile(account_id, card_id, status))
    return payment_profile


def create_user_profile(account_id: UUID, status: Status) -> UserProfile:
    """Creates a Test User Profile."""

    user_profile = UserProfile()
    user_profile.account_id = account_id
    user_profile.status = status
    return user_profile


def create_user_profiles(account_ids: list[UUID]) -> list[UserProfile]:
    """Creates Test User Profiles."""

    user_profiles = []
    for account_id, status in zip(account_ids, STATUSES):
        user_profiles.append(create_user_profile(account_id, status))
    return user_profiles


def create_login(user_id: UUID) -> LoginHistory:
    """Creates a Test Login Profile."""

    login_history = LoginHistory()
    login_history.user_id = user_id
    return login_history


def create_logins(user_ids: list[UUID]) -> list[LoginHistory]:
    """Creates Test User Profiles."""

    logins = []
    for user_id in user_ids:
        logins.append(create_login(user_id))
    return logins
