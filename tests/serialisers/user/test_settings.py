"""User: Testing Settings Profile Serialiser."""

from datetime import datetime, timedelta
from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from lib.interfaces.exceptions import SettingsProfileError
from lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    ProfileVisibility,
    Theme,
    Verification,
)
from models.user.settings import SettingsProfile
from serialisers.user.settings import SettingsProfileSerialiser
from models import ENGINE
from services.authentication import AbstractService
from tests.conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


def test_settingsprofileserialiser_create(get_accounts):
    """Testing Account Serialiser: Create Account."""

    for account in get_accounts:
        with Session(ENGINE) as session:
            settings = SettingsProfileSerialiser().create_settings_profile(account.id)
            settings_id = AbstractService.get_public_id(settings)
            settings = (
                session.query(SettingsProfile)
                .filter(SettingsProfile.settings_id == settings_id)
                .one_or_none()
            )
            assert settings.id is not None

            run_test_teardown([settings], session)


@mark.parametrize("data", check_invalid_ids())
def test_settingsprofileserialiser_create_invalid(data):
    """Testing Account Serialiser: Create Account."""

    with raises((SettingsProfileError, DataError, ProgrammingError)):
        SettingsProfileSerialiser().create_settings_profile(data)


def test_settingsprofileserialiser_get(get_settings):
    """Testing Account Serialiser: Get Account."""

    for settings in get_settings:
        settings_data = SettingsProfileSerialiser().get_settings_profile(
            settings.settings_id
        )

        assert isinstance(settings_data, dict)
        for key in settings_data:
            assert key not in SettingsProfile.__EXCLUDE_ATTRIBUTES__


@mark.parametrize("data", check_invalid_ids())
def test_settingsprofileserialiser_get_invalid(data):
    """Testing Account Serialiser: Get Account."""

    with raises((SettingsProfileError, DataError, ProgrammingError)):
        SettingsProfileSerialiser().get_settings_profile(data)


def test_settingsprofileserialiser_delete(get_settings):
    """Testing Account Serialiser: Delete Account."""

    for settings in get_settings:
        assert (
            SettingsProfileSerialiser()
            .delete_settings_profile(settings.id)
            .startswith("Deleted: ")
        )


@mark.parametrize("data", check_invalid_ids())
def test_settingsprofileserialiser_delete_invalid(data):
    """Testing Account Serialiser: Delete Account."""

    with raises((SettingsProfileError, DataError, ProgrammingError)):
        SettingsProfileSerialiser().delete_settings_profile(data)


@mark.parametrize(
    "data",
    [
        {
            "mfa_enabled": True,
            "location_tracking_enabled": True,
            "cookies_enabled": True,
            "email_status": Verification.VERIFIED,
            "data_sharing_preferences": [
                DataSharingPreference.PROFILE,
                DataSharingPreference.TRANSACTIONS,
            ],
            "communication_preference": Communication.SLACK,
            "theme_preference": Theme.BLUE,
            "profile_visibility_preference": ProfileVisibility.PRIVATE,
            "mfa_last_used_date": datetime.now(),
            "communication_status": Verification.FAILED,
        },
        {
            "email_status": Verification.EXPIRED,
            "data_sharing_preferences": [],
            "communication_preference": Communication.SMS,
            "mfa_last_used_date": datetime.now() + timedelta(days=1),
        },
    ],
)
def test_settingsprofileserialiser_update_valid(get_settings, data):
    """Testing Account Serialiser: Update Account."""

    for settings in get_settings:
        with Session(ENGINE) as session:
            SettingsProfileSerialiser().update_settings_profile(settings.id, **data)
            settings = session.get(SettingsProfile, settings.id)

            for key, value in data.items():
                if key == "data_sharing_preferences":
                    assert isinstance(getattr(settings, key), list)
                    for interest in getattr(settings, key):
                        assert interest in value
                else:
                    assert getattr(settings, key) == value


@mark.parametrize(
    "data",
    [
        {
            "mfa_enabled": "True",
            "location_tracking_enabled": "True",
            "cookies_enabled": "True",
            "email_status": "VERIFIED",
            "data_sharing_preferences": ["PROFILE", "TRANSACTIONS"],
            "communication_preference": "SLACK",
            "theme_preference": "BLUE",
            "profile_visibility_preference": "PRIVATE",
            "mfa_last_used_date": "2022-05-05",
            "communication_status": "FAILED",
        },
        {
            "mfa_enabled": None,
            "location_tracking_enabled": None,
            "cookies_enabled": None,
            "email_status": None,
            "data_sharing_preferences": [None, None],
            "communication_preference": None,
            "theme_preference": None,
            "profile_visibility_preference": None,
            "mfa_last_used_date": None,
            "communication_status": None,
        },
        {
            "data_sharing_preferences": "[None, None]",
        },
        {
            "data_sharing_preferences": None,
        },
    ],
)
def test_settingsprofileserialiser_update_invalid(get_settings, data):
    """Testing Account Serialiser: Update Account."""

    for settings in get_settings:
        with raises((SettingsProfileError, DataError, ProgrammingError)):
            SettingsProfileSerialiser().update_settings_profile(settings.id, **data)
