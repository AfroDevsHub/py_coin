"""Validators: Testing Invalid User Module."""

from datetime import date, datetime
from random import randint
from typing import Any

from pytest import mark, raises
from src.lib.types.exceptions import (
    CardValidationError,
    PaymentProfileError,
    SettingsProfileError,
    UserError,
    UserProfileError,
)
from lib.utils.constants.users import (
    CardType,
    DataSharingPreference,
    ProfileVisibility,
    SocialMediaLink,
    Status,
)
from lib.validators.users import (
    validate_email,
    validate_balance,
    validate_biography,
    validate_card_number,
    validate_card_type,
    validate_cvv_number,
    validate_data_sharing_preferences,
    validate_date_of_birth,
    validate_description,
    validate_first_name,
    validate_interests,
    validate_last_name,
    validate_mobile_number,
    validate_name,
    validate_password,
    validate_pin,
    validate_profile_visibility_preference,
    validate_social_media_links,
    validate_status,
    validate_username,
)

LENGTH_DATA = {"socials": len(list(SocialMediaLink))}


@mark.parametrize(
    "email",
    ["testing123test.com", "testing321#test.com"],
)
def test_invalidate_email_invalid(email: str) -> None:
    """Tests Invalidating Email."""

    with raises(UserError):
        validate_email(email)


@mark.parametrize(
    "password",
    ["password", "_#15"],
)
def test_invalidate_password_invalid(password: str) -> None:
    """Tests Invalidating Password."""

    with raises(UserError):
        validate_password(password)


@mark.parametrize(
    "status",
    [Status.DISABLED, Status.INACTIVE],
)
def test_invalidate_status_invalid(status: Status) -> None:
    """Tests Invalidating User Status."""

    with raises(UserError):
        validate_status(status)


@mark.parametrize(
    "data",
    [
        "Welcome",
        1,
        ProfileVisibility.ADMIN,
        0,
    ],
)
def test_invalidate_data_sharing_preferences_invalid(data: Any) -> None:
    """Tests Invalidating User Data Sharing."""

    with raises(SettingsProfileError):
        validate_data_sharing_preferences(data)


@mark.parametrize(
    "visiblity",
    [ProfileVisibility.ADMIN],
)
def test_invalidate_profile_visibility_preference_invalid(visiblity: ProfileVisibility) -> None:
    """Tests Invalidating Profile Visibility."""

    with raises(SettingsProfileError):
        validate_profile_visibility_preference(visiblity)


@mark.parametrize(
    "firstname",
    ["1", 1, "123Testingname", "TestingName@123", Status.ACTIVE],
)
def test_invalidate_first_name(firstname: Any) -> None:
    """Tests Invalidating First Name."""

    with raises(UserProfileError):
        validate_first_name(firstname)


@mark.parametrize(
    "lastname",
    [2, "2", "12343Testinglastname", "@#TestingLastName_", "LASTNAME___"],
)
def test_invalidate_last_name(lastname: Any) -> None:
    """Tests Invalidating Last Name."""

    with raises(UserProfileError):
        validate_last_name(lastname)


@mark.parametrize(
    "username",
    [
        "username",
        "123usernames",
        "123456",
        "testusermname?",
        "??????????",
        "          ",
        10000,
    ],
)
def test_invalidate_username(username: Any) -> None:
    """Tests Invalidating Username."""

    with raises(UserError):
        validate_username(username)


@mark.parametrize(
    "dob",
    ["date(1991, 12, 31)", date(2008, 12, 31), datetime(1966, 5, 15, 1, 1, 1)],
)
def test_invalidate_date_of_birth(dob: Any) -> None:
    """Tests Invalidating Date Of Birth."""

    with raises((UserProfileError, TypeError)):
        validate_date_of_birth(dob)


@mark.parametrize(
    "mobile",
    ["06685642078", "0685642078", 5685642078, "4564"],
)
def test_invalidate_mobile_number(mobile: Any) -> None:
    """Tests Invalidating Mobile Number."""

    with raises(UserProfileError):
        validate_mobile_number(mobile)


@mark.parametrize(
    "bio",
    [
        "Longer.",
        "=1235=",
        "                           ",
    ],
)
def test_invalidate_biography(bio: str) -> None:
    """Tests Invalidating Biography."""

    with raises((UserProfileError, TypeError)):
        validate_biography(bio)


@mark.parametrize(
    "data",
    [
        "SPORTS",
        "Sports",
        123,
        DataSharingPreference.ACCOUNT,
    ],
)
def test_invalidate_interests(data: Any) -> None:
    """Tests Invalidating Profile Interests."""

    with raises(UserProfileError):
        validate_interests(data)


@mark.parametrize(
    "data",
    [
        LENGTH_DATA["socials"] - randint(1, LENGTH_DATA["socials"]),
        LENGTH_DATA["socials"] - randint(1, LENGTH_DATA["socials"]),
        LENGTH_DATA["socials"] - randint(1, LENGTH_DATA["socials"]),
        0,
    ],
)
def test_invalidate_social_media_links(get_socials: dict[str, str], data: int) -> None:
    """Tests Invalidating Social Media Links."""

    result = {link: get_socials[link] for link in list(get_socials)[0:data]}
    assert not validate_social_media_links(result)


@mark.parametrize(
    "names",
    [
        "card",
        "1234cardnames",
        "@test card_name",
        "#$Tes",
        1.0,
        CardType.CHEQUE,
    ],
)
def test_invalidate_name(names: Any) -> None:
    """Tests Invalidating Card Name."""

    with raises(UserError):
        validate_name(names)


@mark.parametrize(
    "description",
    ["123Longer", "Long", "@#Long", 1, CardType.CREDIT],
)
def test_invalidate_description(description: Any) -> None:
    """Tests Invalidating Card Description."""

    with raises(UserError):
        validate_description(description)


@mark.parametrize(
    "balance",
    [0.0, 0, -5.0, -50.0, "50.0", "Welcome"],
)
def test_invalidate_balance(balance: Any) -> None:
    """Tests Invalidating Card Balance."""

    with raises(PaymentProfileError):
        assert validate_balance(balance) == balance


@mark.parametrize("data", ["list(CardType)", 1, "Cheque"])
def test_invalidate_card_type(data: Any) -> None:
    """Tests Invalidating Card Type."""

    with raises(CardValidationError):
        validate_card_type(data)


@mark.parametrize(
    "number",
    [1991123456789, "123456788", "19911234567861991123456787", CardType.SAVINGS],
)
def test_invalidate_card_number(number: Any) -> None:
    """Tests Invalidating Card Number."""

    with raises(CardValidationError):
        validate_card_number(number)


@mark.parametrize(
    "cvv",
    [123, 321, "def", CardValidationError],
)
def test_invalidate_cvv_number(cvv: Any) -> None:
    """Tests Invalidating CVV Number."""

    with raises(CardValidationError):
        validate_cvv_number(cvv)


@mark.parametrize(
    "pin",
    [123456, 199112, "def725", "DEL123", "123"],
)
def test_invalidate_pin(pin: Any) -> None:
    """Tests Invalidating Card Pin."""

    with raises(CardValidationError):
        validate_pin(pin)
