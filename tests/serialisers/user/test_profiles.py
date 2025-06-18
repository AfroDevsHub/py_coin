"""User: Testing User Profile Serialiser."""

from base64 import b64encode
from datetime import date
from re import compile as regex_compile
from uuid import uuid4

from pydantic import ValidationError
from pytest import mark, raises
from lib.types.user import ProfileData
from services.authentication import AbstractService
from tests.test_utils.utils import generate_socials, check_invalid_ids
from sqlalchemy import cast, String
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from lib.exceptions import UserError, UserProfileError
from lib.utils.constants.users import (
    Country,
    Gender,
    Interest,
    Language,
    Occupation,
    SocialMediaLink,
    Status,
)
from models.user.profiles import UserProfile
from serialisers.user.profiles import UserProfileSerialiser
from models import ENGINE
from tests.conftest import run_test_teardown


def __read_file__():
    """Util Function to Read the sample File."""
    with open("tests/test_profile.png", "rb") as file:
        return b64encode(file.read())


def test_userprofileserialiser_create(get_accounts):
    """Testing UserProfile Serialiser: Create UserProfile."""

    for account in get_accounts:
        with Session(ENGINE) as session:
            user_profile = UserProfileSerialiser().create_user_profile(account.id)
            user_profile_id = AbstractService.get_public_id(user_profile)
            user_profile = (
                session.query(UserProfile)
                .filter(cast(UserProfile.profile_id, String) == user_profile_id)
                .one_or_none()
            )
            assert user_profile.id is not None
            run_test_teardown({user_profile}, session)


@mark.parametrize("data", check_invalid_ids())
def test_userprofileserialiser_create_kwargs_invalid(data):
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises((UserProfileError, DataError, ProgrammingError)):
        UserProfileSerialiser().create_user_profile(data)


def test_userprofileserialiser_get(get_profiles):
    """Testing UserProfile Serialiser: Get UserProfile."""

    for profile in get_profiles:
        user_profile_data = UserProfileSerialiser().get_user_profile(profile.profile_id)

        assert isinstance(user_profile_data, dict)
        for key in user_profile_data:
            assert key not in UserProfile.__EXCLUDE_ATTRIBUTES__


@mark.parametrize("data", check_invalid_ids())
def test_userprofileserialiser_get_kwargs_invalid(data):
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises((UserProfileError, DataError, ProgrammingError)):
        UserProfileSerialiser().get_user_profile(data)


def test_userprofileserialiser_delete(get_profiles):
    """Testing UserProfile Serialiser: Delete UserProfile."""

    for profile in get_profiles:
        assert (
            UserProfileSerialiser()
            .delete_user_profile(profile.id)
            .startswith("Deleted: ")
        )


@mark.parametrize("data", check_invalid_ids())
def test_userprofileserialiser_delete_kwargs_invalid(data):
    """Testing UserProfile Serialiser: Create UserProfile."""

    with raises((UserProfileError, DataError, ProgrammingError)):
        UserProfileSerialiser().delete_user_profile(data)


@mark.parametrize(
    "data",
    [
        {
            "first_name": "validfirstname",
            "last_name": "validlastname",
            "username": "validusername_123-dave",
            "date_of_birth": date(1991, 12, 31),
            "mobile_number": "+27685642078",
            "biography": "Longer Description for a Biography for testing.",
            "country": Country.AFGHANISTAN,
            "language": Language.AFRIKAANS,
            "occupation": Occupation.ACCOUNTANT,
            "status": Status.ACTIVE,
            "gender": Gender.FEMALE,
            "interests": [Interest.ANIMALS],
            "social_media_links": {
                SocialMediaLink.GITHUB: generate_socials("GITHUB"),
                SocialMediaLink.TIKTOK: generate_socials("TIKTOK"),
                SocialMediaLink.SPOTIFY: generate_socials("SPOTIFY"),
            },
            "profile_picture": __read_file__(),
        },
        {
            "first_name": "Testfirstname",
            "last_name": "Testlastname",
            "username": "Testusername#123",
            "date_of_birth": date(2006, 2, 14),
            "mobile_number": "+566685642078",
            "status": Status.DELETED,
            "interests": [],
            "social_media_links": {},
        },
        {
            "status": Status.NEW,
            "interests": [Interest.ANIMALS, Interest.CALLIGRAPHY, Interest.COFFEE],
            "social_media_links": {
                SocialMediaLink.SOUNDCLOUD: generate_socials("SOUNDCLOUD"),
                SocialMediaLink.INSTAGRAM: generate_socials("INSTAGRAM"),
                SocialMediaLink.SLACK: generate_socials("SLACK"),
            },
        },
    ],
)
def test_userprofileserialiser_update_valid(get_profiles, data):
    """Testing UserProfile Serialiser: Update UserProfile."""

    for profile in get_profiles:
        with Session(ENGINE) as session:
            UserProfileSerialiser().update_user_profile(profile.id, ProfileData(**data))
        profile = session.get(UserProfile, profile.id)

        for key, value in data.items():
            if key == "social_media_links":
                assert getattr(profile, key) == {k.name: v for k, v in value.items()}
            elif key == "interests":
                assert isinstance(getattr(profile, key), list)
                for interest in getattr(profile, key):
                    assert interest in value
            else:
                assert getattr(profile, key) == value


@mark.parametrize(
    "data",
    [
        {
            "first_name": "invalid",
            "last_name": "invalid",
            "username": "invalid",
            "date_of_birth": date.today(),
            "mobile_number": "0685642078",
            "biography": "Longer",
            "country": "AFGHANISTAN",
            "language": "AFRIKAANS",
            "occupation": "ACCOUNTANT",
            "status": Status.DISABLED,
            "gender": "MALE",
            "interests": ["ANIMALS"],
            "social_media_links": {"GITHUB": "https://github.com/testing"},
            "profile_picture": 123456789,
        },
        {
            "first_name": "1invalid",
            "last_name": "2invalid",
            "username": "@12323213invalid",
            "date_of_birth": "2020-05-05",
            "mobile_number": "cellphonenumber",
            "biography": "1234567",
            "status": 2353,
            "interests": 1,
            "social_media_links": {12345: "https://github.com/testing"},
            "profile_picture": "Any Valid String",
        },
        {
            "first_name": 123,
            "last_name": 4567,
            "username": 124234,
            "social_media_links": "Invalid Dict.",
        },
        {
            "first_name": None,
            "last_name": None,
            "username": None,
            "date_of_birth": None,
            "mobile_number": None,
            "biography": None,
            "country": None,
            "language": None,
            "occupation": None,
            "status": None,
            "gender": None,
            "interests": None,
            "social_media_links": None,
            "profile_picture": None,
        },
    ],
)
def test_userprofileserialiser_update_invalid(get_profiles, data):
    """Testing UserProfile Serialiser: Update UserProfile."""

    for profile in get_profiles:
        with raises((UserProfileError, UserError, ValidationError)):
            UserProfileSerialiser().update_user_profile(profile.id, ProfileData(**data))
