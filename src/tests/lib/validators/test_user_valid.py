"""Validators: Testing Valid User Module."""

from datetime import date
from random import randint

from pytest import mark
from lib.utils.constants.users import (
    CardType,
    DataSharingPreference,
    Interest,
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

LENGTH_DATA = {
    "data": len(list(DataSharingPreference)),
    "interests": len(list(Interest)),
    "socials": len(list(SocialMediaLink)),
}


@mark.parametrize(
    "email",
    ["testing123@test.com", "testing321@test.com"],
)
def test_validate_email(email):
    """Tests Validating Email."""

    assert validate_email(email) == email


@mark.parametrize(
    "password",
    ["password@1234", "password_#15"],
)
def test_validate_password(password):
    """Tests Validating Password."""

    assert validate_password(password) == password


@mark.parametrize(
    "status",
    [Status.NEW, Status.ACTIVE, Status.DELETED],
)
def test_validate_status(status):
    """Tests Validating User Status."""

    assert validate_status(status) == status


@mark.parametrize(
    "data",
    [
        LENGTH_DATA["data"] - randint(1, LENGTH_DATA["data"]),
        LENGTH_DATA["data"] - randint(1, LENGTH_DATA["data"]),
        LENGTH_DATA["data"] - randint(1, LENGTH_DATA["data"]),
        0,
    ],
)
def test_validate_data_sharing_preferences(data):
    """Tests Validating User Data Sharing."""

    data = list(DataSharingPreference)[0:data]
    assert isinstance(validate_data_sharing_preferences(data), list)


@mark.parametrize(
    "visiblity",
    [ProfileVisibility.PRIVATE, ProfileVisibility.PUBLIC],
)
def test_validate_profile_visibility_preference(visiblity):
    """Tests Validating Profile Visibility."""

    assert validate_profile_visibility_preference(visiblity) == visiblity


@mark.parametrize(
    "firstname",
    ["firstname", "testname", "Testingname", "TestingName", "FIRSTNAME"],
)
def test_validate_first_name(firstname):
    """Tests Validating First Name."""

    assert validate_first_name(firstname) == firstname


@mark.parametrize(
    "lastname",
    ["lastname", "testlastname", "Testinglastname", "TestingLastName", "LASTNAME"],
)
def test_validate_last_name(lastname):
    """Tests Validating Last Name."""

    assert validate_last_name(lastname) == lastname


@mark.parametrize(
    "username",
    [
        "username#123",
        "usernames",
        "test username",
        "Testing@username",
        "Testing-LastName",
        "LAST_NAME",
    ],
)
def test_validate_username(username):
    """Tests Validating Username."""

    assert validate_username(username) == username


@mark.parametrize(
    "dob",
    [date(1991, 12, 31), date(2004, 12, 31), date(1966, 5, 15)],
)
def test_validate_date_of_birth(dob):
    """Tests Validating Date Of Birth."""

    assert validate_date_of_birth(dob) == dob


@mark.parametrize(
    "mobile",
    ["+566685642078", "+27685642078", "+275685642078"],
)
def test_validate_mobile_number(mobile):
    """Tests Validating Mobile Number."""

    assert validate_mobile_number(mobile) == mobile


@mark.parametrize(
    "bio",
    [
        "Longer Description That serves as atest Biography.",
        "1235 Longer Description.",
        "Why would 1 even need a test bio?",
    ],
)
def test_validate_biography(bio):
    """Tests Validating Biography."""

    assert validate_biography(bio) == bio


@mark.parametrize(
    "data",
    [
        LENGTH_DATA["interests"] - randint(1, LENGTH_DATA["interests"]),
        LENGTH_DATA["interests"] - randint(1, LENGTH_DATA["interests"]),
        LENGTH_DATA["interests"] - randint(1, LENGTH_DATA["interests"]),
        0,
    ],
)
def test_validate_interests(data):
    """Tests Validating Profile Interests."""

    data = list(Interest)[0:data]
    assert isinstance(validate_interests(data), list)


@mark.parametrize(
    "data",
    [
        LENGTH_DATA["socials"] - randint(1, LENGTH_DATA["socials"]),
        LENGTH_DATA["socials"] - randint(1, LENGTH_DATA["socials"]),
        LENGTH_DATA["socials"] - randint(1, LENGTH_DATA["socials"]),
        0,
    ],
)
def test_validate_social_media_links(get_socials, data):
    """Tests Validating Social Media Links."""

    data = {link: get_socials[link.name] for link in list(SocialMediaLink)[0:data]}
    assert validate_social_media_links(data) == {k.name: v for k, v in data.items()}


@mark.parametrize(
    "names",
    [
        "card#123@",
        "cardnames",
        "test card_name",
        "Testing@cardname",
        "Testing-cardName",
        "CARD_NAME",
    ],
)
def test_validate_name(names):
    """Tests Validating Card Name."""

    assert validate_name(names) == names


@mark.parametrize(
    "description",
    [
        "Longer Description That serves as atest Biography.",
        "Longer 1235 Description.",
        "Why would 1 even need a test bio",
    ],
)
def test_validate_description(description):
    """Tests Validating Card Description."""

    assert validate_description(description) == description


@mark.parametrize(
    "balance",
    [0.1, 1.0, 5.0, 50.0],
)
def test_validate_balance(balance):
    """Tests Validating Card Balance."""

    assert validate_balance(balance) == balance


@mark.parametrize("data", list(CardType))
def test_validate_card_type(data):
    """Tests Validating Card Type."""

    assert validate_card_type(data) == data


@mark.parametrize(
    "number",
    ["1991123456789", "1991123456788", "1991123456786", "1991123456787"],
)
def test_validate_card_number(number):
    """Tests Validating Card Number."""

    assert validate_card_number(number) == number


@mark.parametrize(
    "cvv",
    ["123", "321", "469", "199"],
)
def test_validate_cvv_number(cvv):
    """Tests Validating CVV Number."""

    assert validate_cvv_number(cvv) == cvv


@mark.parametrize(
    "pin",
    ["123456", "199112", "189725", "968544"],
)
def test_validate_pin(pin):
    """Tests Validating Card Pin."""

    assert validate_pin(pin) == pin
