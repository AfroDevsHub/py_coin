"""Profiles: Serialiser for User Profile Model."""

from typing import Union
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
<<<<<<< HEAD
from lib.exceptions import UserProfileError
from lib.types.user import ProfileData
=======
from pydantic import validate_call
from lib.interfaces.exceptions import UserProfileError
from lib.interfaces.user.profiles import CreateUserProfileData, UpdateUserProfileData
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from models import ENGINE
from models.user.profiles import UserProfile
from serialisers.serialiser import ISerialiser




class UserProfileSerialiser(ISerialiser):
    """Serialiser for the User Profile Model."""

<<<<<<< HEAD
    __SERIALISER_EXCEPTION__ = UserProfileError
    __MUTABLE_KWARGS__: list[str] = [
        "first_name",
        "last_name",
        "username",
        "date_of_birth",
        "gender",
        "profile_picture",
        "mobile_number",
        "country",
        "language",
        "biography",
        "occupation",
        "interests",
        "social_media_links",
        "status",
    ]

    def get_user_profile(self, profile_id: UUID) -> dict[str, Any]:
=======
    @validate_call
    def read(self, model_id: UUID) -> UserProfile:
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
        """CRUD Operation: Get User Profile."""

        with Session(ENGINE) as session:
            user_profile = session.get(UserProfile, model_id)

            if not user_profile:
                raise UserProfileError("User Profile not Found.")

            return user_profile

    @validate_call
    def create(self, data: CreateUserProfileData) -> UserProfile:
        """CRUD Operation: Add User Profile."""

        with Session(ENGINE) as session:
            user_profile = UserProfile(account_id=data.account_id)

            try:
                session.add(user_profile)
                session.commit()
                session.refresh(user_profile)
            except IntegrityError as exc:
                raise UserProfileError("User Profile Not Created.") from exc

            return user_profile

<<<<<<< HEAD
    def update_user_profile(self, private_id: UUID, data: ProfileData) -> str:
=======
    @validate_call
    def update(self, model_id: UUID, data: UpdateUserProfileData) -> UserProfile:
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
        """CRUD Operation: Update User Profile."""

        with Session(ENGINE) as session:
            user_profile: Union[UserProfile, UserProfileError, None] = session.get(
                UserProfile, model_id
            )

            if user_profile is None:
                raise UserProfileError("User Profile Not Found.")

            for key, value in data.model_dump().items():
<<<<<<< HEAD
                setattr(user_profile, key, value)
=======
                if value is not None:
                    setattr(user_profile, key, value)

>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
            try:
                session.add(user_profile)
                session.commit()
            except IntegrityError as exc:
                raise UserProfileError("User Profile not Updated.") from exc

            return user_profile

    @validate_call
    def delete(self, model_id: UUID) -> str:
        """CRUD Operation: Delete User Profile."""

        with Session(ENGINE) as session:
            user_profile = session.get(UserProfile, model_id)

            if not user_profile:
                raise UserProfileError("User Profile Not Found")

            try:
                session.delete(user_profile)
                session.commit()
            except IntegrityError as exc:
                raise UserProfileError("User Profile not Deleted") from exc

            return f"Deleted: {model_id}"
