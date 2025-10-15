from datetime import date, timedelta
from uuid import UUID
from pydantic import BaseModel, field_validator

from src.lib.types.exceptions import UserProfileError
from src.lib.utils.constants.users import (
    Country,
    Gender,
    Interest,
    Language,
    Occupation,
    Regex,
    SocialMediaLink,
    Status,
)


class CreateUserProfileData(BaseModel):
    """Data Model for User Profile Creation."""

    account_id: UUID


class UpdateUserProfileData(BaseModel):
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
