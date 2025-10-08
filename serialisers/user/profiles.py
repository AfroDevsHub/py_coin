"""Profiles: Serialiser for User Profile Model."""

from typing import Union
from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from lib.exceptions import UserProfileError
from lib.types.user import ProfileData
from models import ENGINE
from models.user.profiles import UserProfile
from serialisers.serialiser import BaseSerialiser


class UserProfileSerialiser(UserProfile, BaseSerialiser):
    """Serialiser for the User Profile Model."""

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
        """CRUD Operation: Get User Profile."""

        with Session(ENGINE) as session:
            query = select(UserProfile).filter(cast(UserProfile.profile_id, uuid) == profile_id)
            user_profile = session.execute(query).scalar_one_or_none()

            if not user_profile:
                raise UserProfileError("User Profile not Found.")

            return self.__get_model_data__(user_profile)

    def create_user_profile(self, account_id: UUID) -> str:
        """CRUD Operation: Add User Profile."""

        with Session(ENGINE) as session:
            self.account_id = account_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise UserProfileError("User Profile Not Created.") from exc

            return str(self)

    def update_user_profile(self, private_id: UUID, data: ProfileData) -> str:
        """CRUD Operation: Update User Profile."""

        with Session(ENGINE) as session:
            user_profile: Union[UserProfile, UserProfileError, None] = session.get(
                UserProfile, private_id
            )

            if user_profile is None:
                raise UserProfileError("User Profile Not Found.")

            for key, value in data.model_dump().items():
                setattr(user_profile, key, value)
            try:
                session.add(user_profile)
                session.commit()
            except IntegrityError as exc:
                raise UserProfileError("User Profile not Updated.") from exc

            return str(user_profile)

    def delete_user_profile(self, private_id: UUID) -> str:
        """CRUD Operation: Delete User Profile."""

        with Session(ENGINE) as session:
            user_profile = session.get(UserProfile, private_id)

            if not user_profile:
                raise UserProfileError("User Profile Not Found")

            try:
                session.delete(user_profile)
                session.commit()
            except IntegrityError as exc:
                raise UserProfileError("User Profile not Deleted") from exc

            return f"Deleted: {private_id}"
