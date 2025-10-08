from uuid import UUID
from pydantic import BaseModel, field_validator

from lib.interfaces.exceptions import (
    AccountError,
)
from lib.utils.constants.users import (
    Status,
)

class CreateAccountData(BaseModel):
    """Data Model for Account Creation."""

    user_id: UUID


class UpdateAccountData(BaseModel):
    """Data Model for Account Update."""

    status: Status | None = None

    @field_validator("status")
    def validate_status(cls, value: Status) -> Status:
        """Validate Account Status."""

        if value not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
            raise AccountError("Invalid Status.")

        return value