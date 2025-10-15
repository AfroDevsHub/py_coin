"""Profiles: Serialiser for User Profile Model."""

from typing import Union
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import validate_call

from src.lib.types.exceptions import UserProfileError
from src.lib.types.user.profiles import CreateUserProfileData, UpdateUserProfileData
from src.models import ENGINE
from src.models.user.profiles import UserProfile
from src.serialisers.serialiser import ISerialiser




class UserProfileSerialiser(ISerialiser):
    """Serialiser for the User Profile Model."""

    @validate_call
    def read(self, model_id: UUID) -> UserProfile:
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

    @validate_call
    def update(self, model_id: UUID, data: UpdateUserProfileData) -> UserProfile:
        """CRUD Operation: Update User Profile."""

        with Session(ENGINE) as session:
            user_profile: Union[UserProfile, UserProfileError, None] = session.get(
                UserProfile, model_id
            )

            if user_profile is None:
                raise UserProfileError("User Profile Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(user_profile, key, value)

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
