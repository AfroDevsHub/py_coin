from pydantic import BaseModel, field_validator

from src.lib.types.exceptions import UserError
from src.lib.utils.constants.users import (
    Regex,
    Status,
)


class CreateUserData(BaseModel):
    """Data Model for User Creation."""

    email: str
    password: str

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        """Validate User Email."""

        if not Regex.EMAIL.value.match(value):
            raise UserError("Invalid Email.")

        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """Validate User Password."""

        if not Regex.PASSWORD.value.match(value):
            raise UserError("Invalid Password.")

        return value


class UpdateUserData(BaseModel):
    """Data Model for User Update."""

    status: Status | None = None
    password: str | None = None

    @field_validator("status")
    def validate_status(cls, value: Status) -> Status:
        """Validate User Status."""

        if value not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
            raise UserError("Invalid Status.")

        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """Validate User Password."""

        if not Regex.PASSWORD.value.match(value):
            raise UserError("Invalid Password.")

        return value




