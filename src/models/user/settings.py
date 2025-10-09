"""Settings: Settings Profile Model."""

from uuid import uuid4
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    ARRAY,
    text,
)

from src.lib.utils.constants.users import (
    Communication,
    DataSharingPreference,
    Verification,
    ProfileVisibility,
    Theme,
)
from src.models import Base


class SettingsProfile(Base):
    """Model representing a User's Settings."""

    __tablename__ = "settings_profiles"
    __table_args__ = ({"schema": "users"},)

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid4,
        unique=True,
    )
    settings_id = Column(
        "settings_id", UUID(as_uuid=True), nullable=False, default=uuid4, unique=True
    )
    account_id = Column(
        "account_id",
        UUID(as_uuid=True),
        ForeignKey("users.accounts.id"),
        nullable=False,
        unique=True,
    )
    email_status: Verification | Column[Verification] = Column(
        "email_status",
        Enum(Verification, name="email_verification"),
        default=Verification.UNVERIFIED,
        nullable=False,
    )
    communication_status: Verification | Column[Verification] = Column(
        "communication_status",
        Enum(Verification, name="communication_verification"),
        default=Verification.UNVERIFIED,
        nullable=False,
    )
    mfa_enabled = Column("mfa_enabled", Boolean, default=False, nullable=False)
    mfa_last_used_date = Column("mfa_last_used_date", DateTime, nullable=True)
    profile_visibility_preference: ProfileVisibility | Column[ProfileVisibility] = (
        Column(
            "profile_visibility_preference",
            Enum(ProfileVisibility, name="profilevisibility"),
            default=ProfileVisibility.PUBLIC,
            nullable=False,
        )
    )
    data_sharing_preferences: (
        list[DataSharingPreference] | Column[list[DataSharingPreference]]
    ) = Column(
        "data_sharing_preferences",
        ARRAY(Enum(DataSharingPreference, name="data_sharing_preference")),
        default=[DataSharingPreference.ACCOUNT],
        nullable=False,
    )
    communication_preference: Communication | Column[Communication] = Column(
        "communication_preference",
        Enum(Communication, name="communication"),
        default=Communication.EMAIL,
        nullable=False,
    )
    location_tracking_enabled = Column(
        "location_tracking_enabled", Boolean, default=False, nullable=False
    )
    cookies_enabled = Column("cookies_enabled", Boolean, default=False, nullable=False)
    theme_preference: Theme | Column[Theme] = Column(
        "theme_preference",
        Enum(Theme, name="theme"),
        nullable=False,
        default=Theme.LIGHT,
    )
    created_date = Column(
        "created_date", DateTime, default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_date = Column(
        "updated_date",
        DateTime,
        default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    def __str__(self) -> str:
        """String Representation of the Settings Object."""

        return f"Settings ID: {str(self.settings_id)}, Account ID: {self.account_id}, Email Status: {self.email_status}, Communication Status: {self.communication_status}, MFA Enabled: {self.mfa_enabled}, Profile Visibility: {self.profile_visibility_preference}, Data Sharing Preferences: {self.data_sharing_preferences}, Communication Preference: {self.communication_preference}, Location Tracking: {self.location_tracking_enabled}, Cookies Enabled: {self.cookies_enabled}, Theme Preference: {self.theme_preference}"

    def __repr__(self) -> str:
        """String Representation of the Settings Object."""

        return f"SettingsProfile({self.settings_id}, {self.account_id}, {self.email_status}, {self.communication_status}, {self.mfa_enabled}, {self.profile_visibility_preference}, {self.data_sharing_preferences}, {self.communication_preference}, {self.location_tracking_enabled}, {self.cookies_enabled}, {self.theme_preference})"
