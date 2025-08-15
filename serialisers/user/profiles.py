"""Profiles: Serialiser for User Profile Model."""

from datetime import date, timedelta
from typing import Any, Union
from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, field_validator, validate_call, validate_call
from lib.interfaces.exceptions import UserProfileError
from lib.utils.constants.users import (
    Country,
    Gender,
    Interest,
    Language,
    Occupation,
    Regex,
    SocialMediaLink,
    Status,
)
from models import ENGINE
from models.user.profiles import UserProfile
from serialisers.serialiser import BaseSerialiser


class UpdateUserProfile(BaseModel):
    """Data Model for User Profile Update."""

    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    profile_picture: str | None = None
    mobile_number: str | None = None
    country: Country | None = None
    language: Language | None = None
    biography: str | None = None
    occupation: Occupation | None = None
    interests: list[Interest] | None = None
    social_media_links: dict[SocialMediaLink, str] | None = None
    status: Status | None = None

    @field_validator("first_name")
    def validate_first_name(cls, value: str) -> str:
        """Validate User Profile First Name."""
        if not Regex.NAME.value.match(value):
            raise UserProfileError("Invalid First Name.")
        return value

    @field_validator("last_name")
    def validate_last_name(cls, value: str) -> str:
        """Validate User Profile Last Name."""
        if not Regex.NAME.value.match(value):
            raise UserProfileError("Invalid Last Name.")
        return value

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        """Validate User Profile Username."""
        if not Regex.USERNAME.value.match(value):
            raise UserProfileError("Invalid Username.")
        return value

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value: date) -> date:
        """Validate User Profile Date of Birth."""
        if value > date.today() - timedelta(days=18 * 365):
            raise UserProfileError("invalid Date of Birth.")

        return value

    @field_validator("mobile_number")
    def validate_mobile_number(cls, value: str) -> str:
        """Validate User Profile Mobile Number."""
        if not Regex.MOBILE_NUMBER.value.match(value):
            raise UserProfileError("Invalid Mobile Number.")

        return value

    @field_validator("status")
    def validate_status(cls, value: Status) -> Status:
        """Validate User Profile Status."""

        if value not in [Status.ACTIVE, Status.INACTIVE, Status.DELETED]:
            raise UserProfileError("Invalid Status.")

        return value

    @field_validator("social_media_links")
    def validate_social_media_links(
        cls, value: dict[SocialMediaLink, str]
    ) -> dict[SocialMediaLink, str]:
        """Validate User Profile Social Media Links."""

        for key, link in value.items():
            if not key.value.match(link):
                raise UserProfileError(f"Invalid {key.value} Link.")

        return value

    @field_validator("biography")
    def validate_biography(cls, value: str) -> str:
        """Validate User Profile Biography."""
        if not Regex.BIOGRAPHY.value.match(value):
            raise UserProfileError("Invalid Biography.")
        return value


class UserProfileSerialiser(UserProfile, BaseSerialiser):
    """Serialiser for the User Profile Model."""

    @validate_call
    def get_user_profile(self, profile_id: str) -> dict[str, Any]:
        """CRUD Operation: Get User Profile."""

        with Session(ENGINE) as session:
            query = select(UserProfile).filter(
                cast(UserProfile.profile_id, uuid) == profile_id
            )
            user_profile = session.execute(query).scalar_one_or_none()

            if not user_profile:
                raise UserProfileError("User Profile not Found.")

            return self.__get_model_data__(user_profile)

    @validate_call
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

    @validate_call
    def update_user_profile(self, private_id: str, data: UpdateUserProfile) -> str:
        """CRUD Operation: Update User Profile."""

        with Session(ENGINE) as session:
            user_profile: Union[UserProfile, UserProfileError, None] = session.get(
                UserProfile, private_id
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

            return str(user_profile)

    @validate_call
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
