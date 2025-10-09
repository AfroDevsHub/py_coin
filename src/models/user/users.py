"""Users: User Model."""

from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Enum, String, text
from sqlalchemy.orm import relationship

from src.models import Base
from src.lib.utils.constants.users import Role, Status
from src.models.warehouse.logins import LoginHistory


class User(Base):
    """Model representing a User."""

    __tablename__ = "users"
    __table_args__ = ({"schema": "users"},)

    id = Column(
        "id", UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4, unique=True
    )
    user_id = Column(
        "user_id", UUID(as_uuid=True), nullable=False, unique=True, default=uuid4
    )
    email = Column("email", String(256), unique=True, nullable=False)
    password = Column("password", String(256), nullable=False)
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
    status: Status | Column[Status] = Column(
        "status", Enum(Status, name="user_status"), nullable=False, default=Status.NEW
    )
    salt_value = Column("salt_value", UUID(as_uuid=True), nullable=False, default=uuid4)
    role: Role | Column[Role] = Column(
        "role", Enum(Role), nullable=False, default=Role.USER
    )
    login_history = relationship(
        LoginHistory, backref="User", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        """String Representation of the User Object."""

        return f"User ID: {str(self.user_id)}, Email: {self.email}, Status: {self.status}, Role: {self.role}"

    def __repr__(self) -> str:
        """Recreates an Object: Representation of the User Object."""

        # returns what how to init the model User()
        return f"User({self.user_id}, {self.email}, {self.status}, {self.role})"
