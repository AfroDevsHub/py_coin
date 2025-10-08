"""Logins: Login History Model."""

from uuid import uuid4
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, text, Enum

from lib.utils.constants.users import Country, LoginMethod
from models import Base


class LoginHistory(Base):
    """Model representing User Login History."""

    __tablename__ = "login_history"
    __table_args__ = ({"schema": "warehouse"},)

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True
    )
    login_id = Column(
        "login_id",
        UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        unique=True
    )
    user_id = Column(
        "user_id", UUID(as_uuid=True), ForeignKey("users.users.id"), nullable=False
    )
    session_id = Column(
        "session_id",
        UUID(as_uuid=True),
        nullable=True,
    )
    login_date = Column(
        "login_date", DateTime, nullable=False, default=text("CURRENT_TIMESTAMP")
    )
    login_location: Country | Column[Country] = Column(
        "login_location", Enum(Country, name="login_country"), nullable=True
    )
    login_device = Column("login_device", String(256), nullable=True)
    login_method: LoginMethod | Column[LoginMethod] = Column(
        "login_method",
        Enum(LoginMethod, name="login_method"),
        nullable=True,
        default=LoginMethod.EMAIL,
    )
    logged_in = Column("logged_in", Boolean, nullable=False, default=True)
    logout_date = Column("logout_date", DateTime, nullable=True)
    authentication_token = Column("authentication_token", String, nullable=True)

    def __str__(self) -> str:
        """String Representation of the Login History Object."""

        return f"Login ID: {str(self.login_id)}, User ID: {self.user_id}, Session ID: {self.session_id}, Login Date: {self.login_date}, Login Location: {self.login_location}, Login Device: {self.login_device}, Login Method: {self.login_method}, Logged In: {self.logged_in}, Logout Date: {self.logout_date}, Authentication Token: {self.authentication_token}"

    def __repr__(self) -> str:
        """String Representation of the Login History Object."""

        return f"LoginHistory({self.login_id}, {self.user_id}, {self.session_id}, {self.login_date}, {self.login_location}, {self.login_device}, {self.login_method}, {self.logged_in}, {self.logout_date}, {self.authentication_token})"
