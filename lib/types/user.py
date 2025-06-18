"""Data-Classes: Custom Data-Type Models."""

from typing import Any, Dict, List
from pydantic import BaseModel, field_validator
from datetime import datetime

from lib.exceptions import AccountError
from lib.utils.constants.users import (
    Communication,
    Country,
    DataSharingPreference,
    Gender,
    Interest,
    Language,
    LoginMethod,
    Occupation,
    ProfileVisibility,
    SocialMediaLink,
    Status,
    Theme,
    Verification,
)


class AccountData(BaseModel):
    """Typed Account Dictionary."""

    status: Status | None

    @field_validator("status")
    @classmethod
    def status(cls, value: Status):
        if value not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
            raise AccountError("Invalid Status.")
        return value


class ProfileData(BaseModel):
    """Typed Profile Dictionary."""

    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    date_of_birth: datetime | None = None
    gender: Gender | None = None
    profile_picture: bytes | None = None
    mobile_number: str | None = None
    country: Country | None = None
    language: Language | None = None
    biography: str | None = None
    occupation: Occupation | None = None
    interests: List[Interest] | None = None
    social_media_links: Dict[SocialMediaLink, str] | None = None
    status: Status | None = None

    def model_post_init(self, context: Any) -> str:
        if self.social_media_links:
            self.social_media_links = {k.name: v for k, v in self.social_media_links.items()}
        

class SettingsData(BaseModel):
    """Typed Settings Dictionary."""

    mfa_enabled: str | None
    location_tracking_enabled: bool | None
    cookies_enabled: bool | None
    email_status: Verification | None
    data_sharing_preferences: DataSharingPreference | None
    communication_preference: Communication | None
    theme_preference: Theme | None
    profile_visibility_preference: ProfileVisibility | None
    mfa_last_used_date: datetime | None
    communication_status: Verification | None


class Logindata(BaseModel):
    """Typed User-Account Dictionary."""

    email: str | None
    password: str | None
    login_location: Country | None
    login_device: str | None
    login_method: LoginMethod | None


class UserData(BaseModel):
    """Type Check for User Data."""

    account: AccountData | None = None
    profile: ProfileData | None = None
    settings: SettingsData | None = None


class UserUpdateData(BaseModel):
    status: Status | None = None
    password: str | None = None
