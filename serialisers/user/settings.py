"""Settings: Serialiser for Settings Profile Model."""

from datetime import datetime
from typing import Any
from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, validate_call
from lib.interfaces.exceptions import (
    SettingsProfileError,
)
from lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    ProfileVisibility,
    Theme,
    Verification,
)
from models import ENGINE
from models.user.settings import SettingsProfile
from serialisers.serialiser import BaseSerialiser


class UpdateSettingsProfile(BaseModel):
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


class SettingsProfileSerialiser(SettingsProfile, BaseSerialiser):
    """Serialiser for the Settings Model."""

    @validate_call
    def get_settings_profile(self, settings_id: str) -> dict[str, Any]:
        """CRUD Operation: Get Settings."""

        with Session(ENGINE) as session:
            query = select(SettingsProfile).filter(
                cast(SettingsProfile.settings_id, uuid) == settings_id
            )
            settings_profile = session.execute(query).scalar_one_or_none()

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found.")

            return self.__get_model_data__(settings_profile)

    @validate_call
    def create_settings_profile(self, account_id: str) -> str:
        """CRUD Operation: Add Settings."""

        with Session(ENGINE) as session:
            self.account_id = UUID(account_id)

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise SettingsProfileError("Settings Not Created.") from exc

            return str(self)

    @validate_call
    def update_settings_profile(
        self, private_id: str, data: UpdateSettingsProfile
    ) -> str:
        """CRUD Operation: Update Settings."""

        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, private_id)

            if settings_profile is None:
                raise SettingsProfileError("Settings Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(settings_profile, key, value)

            try:
                session.add(settings_profile)
                session.commit()
            except IntegrityError as exc:
                raise SettingsProfileError("Settings not Updated.") from exc

            return str(settings_profile)

    @validate_call
    def delete_settings_profile(self, private_id: UUID) -> str:
        """CRUD Operation: Delete Settings."""

        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, private_id)

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found")

            try:
                session.delete(settings_profile)
                session.commit()
            except IntegrityError as exc:
                raise SettingsProfileError("Settings not Deleted.") from exc

            return f"Deleted: {private_id}"
