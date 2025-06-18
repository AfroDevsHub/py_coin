"""Users: validations for User related Models."""

from datetime import date
from config import AppConfig
from lib.exceptions import (
    CardValidationError,
    PaymentProfileError,
    SettingsProfileError,
    UserError,
    UserProfileError,
)
from lib.utils.constants.users import (
    CardType,
    DataSharingPreference,
    Interest,
    ProfileVisibility,
    Regex,
    SocialMediaLink,
    Status,
)


def validate_email(email: str, **_) -> str:
    """Validates Email."""

    if not isinstance(email, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.EMAIL.value.match(email):
        raise UserError("Invalid Email.")
    return email


def validate_password(password: str, **_) -> str:
    """Validates Password."""

    if not isinstance(password, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.PASSWORD.value.match(password):
        raise UserError("Invalid Password.")
    return password


def validate_status(status: Status, **_) -> Status:
    """Validates User Status."""

    if not isinstance(status, Status):
        raise UserError("Invalid Type for this Attribute.")
    if status not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
        raise UserError("Invalid Status.")
    return status


def validate_data_sharing_preferences(
    data_sharing: list[DataSharingPreference], **_
) -> list[DataSharingPreference]:
    """Validates User Data Sharing."""

    if not isinstance(data_sharing, list):
        raise SettingsProfileError("Invalid Type for this Attribute.")
    if not all(
        [
            isinstance(data_sharing_item, DataSharingPreference)
            for data_sharing_item in data_sharing
        ]
    ):
        raise SettingsProfileError("Invalid Data Sharing Preference.")
    return list(set(data_sharing))


def validate_profile_visibility_preference(
    profile_visibility: ProfileVisibility, **_
) -> ProfileVisibility:
    """Validates Profile Visibility."""

    if not isinstance(profile_visibility, ProfileVisibility):
        raise SettingsProfileError("Invalid Type for this Attribute.")
    if profile_visibility in [ProfileVisibility.ADMIN]:
        raise SettingsProfileError("Invalid Profile Visibility Preference.")
    return profile_visibility


def validate_first_name(first_name: str, **_) -> str:
    """Validates First Name."""

    if not isinstance(first_name, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.NAME.value.match(first_name):
        raise UserProfileError("Invalid First Name.")
    return first_name


def validate_last_name(last_name: str, **_) -> str:
    """Validates Last Name."""

    if not isinstance(last_name, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.NAME.value.match(last_name):
        raise UserProfileError("Invalid Last Name.")
    return last_name


def validate_username(username: str, **_) -> str:
    """Validates Username."""

    if not isinstance(username, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.USERNAME.value.match(username):
        raise UserError("Invalid User Information.")
    return username


def validate_date_of_birth(date_of_birth: date, **_) -> date:
    """Validates Date Of Birth."""

    if not isinstance(date_of_birth, date):
        raise UserProfileError("Invalid Type for this Attribute.")
    if date_of_birth > date.today().replace(year=date.today().year - 18):
        raise UserProfileError("invalid Date of Birth.")
    return date_of_birth


def validate_mobile_number(mobile_number: str, **_) -> str:
    """Validates Mobile Number."""

    if not isinstance(mobile_number, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.MOBILE_NUMBER.value.match(mobile_number):
        raise UserProfileError("Invalid Mobile Number.")
    return mobile_number


def validate_biography(biography: str, **_) -> str:
    """Validates Biography."""

    if not isinstance(biography, str):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not Regex.BIOGRAPHY.value.match(biography):
        raise UserProfileError("Invalid Biography.")
    return biography


def validate_interests(profile_interests: list[Interest], **_) -> list[Interest]:
    """Validates Profile Interests."""

    if not isinstance(profile_interests, list):
        raise UserProfileError("Invalid Type for this Attribute.")
    if not all([isinstance(interest, Interest) for interest in profile_interests]):
        raise UserProfileError("Invalid List of Interests.")
    return list(set(profile_interests))


def validate_social_media_links(
    social_media_links: dict[SocialMediaLink, str], **_
) -> dict[str, str]:
    """Validates Social Media Links."""

    if not isinstance(social_media_links, dict):
        raise UserProfileError("Invalid Social Media.")
    response: dict[str, str] = {}
    for key, value in social_media_links.items():
        if isinstance(key, SocialMediaLink) and key.value.match(value):
            response[key.name] = value
    return response


def validate_name(name: str, **_) -> str:
    """Validates Card Name."""

    if not isinstance(name, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.USERNAME.value.match(name):
        raise UserError("Invalid Card Name.")
    return name


def validate_description(description: str, **_) -> str:
    """Validates Card Description."""

    if not isinstance(description, str):
        raise UserError("Invalid Type for this Attribute.")
    if not Regex.DESCRIPTION.value.match(description):
        raise UserError("Invalid Card Description.")
    return description


def validate_balance(amount: float, **_) -> float:
    """Validates Card Balance."""

    if not isinstance(amount, float):
        raise PaymentProfileError("Invalid Type for this Attribute.")
    if amount <= 0.0:
        raise PaymentProfileError("Invalid Card Balance.")
    return amount


def validate_card_type(card_type: CardType, **_) -> CardType:
    """Validates Card Type."""

    if not isinstance(card_type, CardType):
        raise CardValidationError("Invalid Type for this Attribute.")
    return card_type


def validate_card_number(card_number: str, **_) -> str:
    """Validates Card Number."""

    if not isinstance(card_number, str):
        raise CardValidationError("Invalid Type for this Attribute.")
    if len(card_number) != AppConfig().card_length:
        raise CardValidationError("Invalid Card Number.")
    return card_number


def validate_cvv_number(cvv_number: str, **_) -> str:
    """Validates CVV Number."""

    if not isinstance(cvv_number, str):
        raise CardValidationError("Invalid Type for this Attribute.")
    if len(cvv_number) != AppConfig().cvv_length:
        raise CardValidationError("Invalid CVV Number.")
    if not Regex.CVV.value.match(cvv_number):
        raise CardValidationError("Invalid Pin.")
    return cvv_number


def validate_pin(pin: str, **_) -> str:
    """Validates Card Pin."""

    if not isinstance(pin, str):
        raise CardValidationError("Invalid Type for this Attribute.")
    if not Regex.PIN.value.match(pin):
        raise CardValidationError("Invalid Pin.")
    return pin
