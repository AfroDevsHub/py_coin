from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from src.lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    ProfileVisibility,
    Theme,
    Verification,
)

class CreateSettingsProfileData(BaseModel):
    account_id: UUID

class UpdateSettingsProfileData(BaseModel):
    mfa_enabled: bool | None = None
    location_tracking_enabled: bool | None = None
    cookies_enabled: bool | None = None
    email_status: bool | None = None
    data_sharing_preferences: list[DataSharingPreference] | None = None
    communication_preference: Communication | None = None
    theme_preference: Theme | None = None
    profile_visibility_preference: ProfileVisibility | None = None
    mfa_last_used_date: datetime | None = None
    communication_status: Verification | None = None
