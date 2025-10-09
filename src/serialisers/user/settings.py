"""Settings: Serialiser for Settings Profile Model."""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
<<<<<<< HEAD
from lib.exceptions import (
=======
from pydantic import validate_call
from lib.interfaces.exceptions import (
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
    SettingsProfileError,
)
from lib.interfaces.user.settings import (
    CreateSettingsProfileData,
    UpdateSettingsProfileData,
)
from models import ENGINE
from models.user.settings import SettingsProfile
from serialisers.serialiser import ISerialiser


class SettingsProfileSerialiser(ISerialiser):
    """Serialiser for the Settings Model."""

<<<<<<< HEAD
    __SERIALISER_EXCEPTION__ = SettingsProfileError
    __MUTABLE_KWARGS__: list[str] = [
        "mfa_enabled",
        "location_tracking_enabled",
        "cookies_enabled",
        "email_status",
        "data_sharing_preferences",
        "communication_preference",
        "theme_preference",
        "profile_visibility_preference",
        "mfa_last_used_date",
        "communication_status",
    ]

    def get_settings_profile(self, settings_id: UUID) -> dict[str, Any]:
        """CRUD Operation: Get Settings."""

        with Session(ENGINE) as session:
            query = select(SettingsProfile).filter(
                cast(SettingsProfile.settings_id, uuid) == settings_id
            )
            settings_profile = session.execute(query).scalar_one_or_none()

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found.")

            return self.__get_model_data__(settings_profile)

    def create_settings_profile(self, account_id: UUID) -> str:
=======
    @validate_call
    def create(self, data: CreateSettingsProfileData) -> SettingsProfile:
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
        """CRUD Operation: Add Settings."""

        with Session(ENGINE) as session:
            settings_profile = SettingsProfile(account_id=data.account_id)

            try:
                session.add(settings_profile)
                session.commit()
                session.refresh(settings_profile)
            except IntegrityError as exc:
                raise SettingsProfileError("Settings Not Created.") from exc

            return settings_profile

    @validate_call
    def read(self, model_id: UUID) -> SettingsProfile:
        """CRUD Operation: Get Settings."""

        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, model_id)

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found.")

            return settings_profile

    @validate_call
    def update(self, model_id: UUID, data: UpdateSettingsProfileData) -> SettingsProfile:
        """CRUD Operation: Update Settings."""

        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, model_id)

            if settings_profile is None:
                raise SettingsProfileError("Settings Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(settings_profile, key, value)

            try:
                session.add(settings_profile)
                session.commit()
                session.refresh(settings_profile)
            except IntegrityError as exc:
                raise SettingsProfileError("Settings not Updated.") from exc

            return settings_profile

    @validate_call
    def delete(self, model_id: UUID) -> str:
        """CRUD Operation: Delete Settings."""

        with Session(ENGINE) as session:
            settings_profile = session.get(SettingsProfile, model_id)

            if not settings_profile:
                raise SettingsProfileError("Settings Not Found")

            try:
                session.delete(settings_profile)
                session.commit()
            except IntegrityError as exc:
                raise SettingsProfileError("Settings not Deleted.") from exc

            return f"Deleted: {model_id}"
