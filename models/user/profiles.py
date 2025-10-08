"""Profiles: User Profile Model."""

from uuid import uuid4
from sqlalchemy import (
    ARRAY,
    JSON,
    UUID,
    Column,
    Date,
    DateTime,
    ForeignKey,
    LargeBinary,
    String,
    text,
    Enum,
)
from lib.utils.constants.users import (
    Country,
    Language,
    Occupation,
    Gender,
    Interest,
    Status,
)
from models import Base


class UserProfile(Base):
    """Model representing a User's Profile."""

    __tablename__ = "user_profiles"
    __table_args__ = ({"schema": "users"},)

    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        nullable=False,
        primary_key=True,
    )
    profile_id = Column(
        "profile_id",
        UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        unique=True,
    )
    account_id = Column(
        "account_id",
        UUID(as_uuid=True),
        ForeignKey("users.accounts.id"),
        nullable=False,
        unique=True,
    )
    first_name = Column("first_name", String(256), nullable=True)
    last_name = Column("last_name", String(256), nullable=True)
    username = Column("username", String(256), nullable=True)
    date_of_birth = Column("date_of_birth", Date, nullable=True)
    gender: Gender | Column[Gender] = Column(
        "gender", Enum(Gender, name="gender"), nullable=True
    )
    profile_picture = Column("profile_picture", LargeBinary, nullable=True)
    mobile_number = Column("mobile_number", String(256), nullable=True)
    country: Country | Column[Country] = Column(
        "country", Enum(Country, name="account_country"), nullable=True
    )
    language: Language | Column[Language] = Column(
        "language",
        Enum(Language, name="account_language"),
        default=Language.ENGLISH,
        nullable=True,
    )
    biography = Column(
        "biography",
        String(256),
        default="This user has not provided a bio yet.",
        nullable=True,
    )
    occupation: Occupation | Column[Occupation] = Column(
        "occupation",
        Enum(Occupation, name="account_occupation"),
        default=Occupation.OTHER,
        nullable=True,
    )
    interests: list[Interest] | Column[list[Interest]] = Column(
        "interests",
        ARRAY(Enum(Interest, name="profile_interest")),
        default=[],
        nullable=True,
    )
    social_media_links = Column("social_media_links", JSON, default={}, nullable=True)
    status: Status | Column[Status] = Column(
        "status",
        Enum(Status, name="profile_status"),
        default=Status.NEW,
        nullable=False,
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
        """String Representation of the User Profile Object."""

        return f"Profile ID: {str(self.profile_id)}, Account ID: {self.account_id}, First Name: {self.first_name}, Last Name: {self.last_name}, Username: {self.username}, Status: {self.status}"

    def __repr__(self) -> str:
        """String Representation of the User Profile Object."""

        return f"UserProfile({self.profile_id}, {self.account_id}, {self.first_name}, {self.last_name}, {self.username})"
