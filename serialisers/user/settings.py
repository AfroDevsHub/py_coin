"""Settings: Serialiser for Settings Profile Model."""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import validate_call
from lib.interfaces.exceptions import (
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

    @validate_call
    def create(self, data: CreateSettingsProfileData) -> SettingsProfile:
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
