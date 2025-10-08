"""Users: Testing Settings Profile Model."""

from pytest import raises

from sqlalchemy.orm import Session

from lib.utils.constants.users import Communication, Verification
from models import ENGINE
from models.user.settings import SettingsProfile
from conftest import run_test_teardown


def test_valid_settings_profile(get_accounts):
    """Testing Settings Profile With Missing Attributes."""

    for account in get_accounts:
        with Session(ENGINE) as session:
            settings_profile = SettingsProfile()
            settings_profile.account_id = account.id
            session.add(settings_profile)
            session.commit()

            assert settings_profile.id is not None
            assert not settings_profile.mfa_enabled
            assert settings_profile.communication_status == Verification.UNVERIFIED
            assert settings_profile.communication_preference == Communication.EMAIL
            assert not settings_profile.cookies_enabled

            run_test_teardown([settings_profile], session)


def test_settings_profile_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            settings_profile = SettingsProfile("email", "password")
            session.add(settings_profile)
            session.commit()
