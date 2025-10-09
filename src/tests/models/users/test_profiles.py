"""Users: Testing User Profile Model."""

from datetime import date
from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.utils.constants.users import Gender
from models import ENGINE
from models.user.profiles import UserProfile
from conftest import run_test_teardown


def test_user_profile_invalid_no_args():
    """Testing User With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            user_profile = UserProfile()
            session.add(user_profile)
            session.commit()


def test_user_profile_profile_invalid_args():
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            user_profile = UserProfile("email", "password")
            session.add(user_profile)
            session.commit()


def test_user_profile__(get_accounts):
    """Testing User With Missing Attributes."""

    for account in get_accounts:
        with Session(ENGINE) as session:
            user_profile = UserProfile()
            user_profile.account_id = account.id
            user_profile.first_name = "firstname"
            user_profile.last_name = "lastnaame"
            user_profile.username = "username_fl"
            user_profile.date_of_birth = date(1991, 12, 31)
            user_profile.gender = Gender.FEMALE
            session.add(user_profile)
            session.commit()

            assert user_profile.interests == []
            assert user_profile.account_id is not None
            assert user_profile.profile_id is not None
            assert isinstance(user_profile.to_dict(), dict)
            assert user_profile.social_media_links == {}

            run_test_teardown([user_profile], session)
