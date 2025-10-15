from uuid import UUID
from pydantic import BaseModel, field_validator

from src.lib.types.exceptions import PaymentProfileError
from src.lib.utils.constants.users import (
    Status,
)


class CreatePaymentProfileData(BaseModel):
    account_id: UUID
    card_id: UUID


class UpdatePaymentProfileData(BaseModel):
    """Data Model for Payment Profile Update."""

    name: str | None = None
    description: str | None = None
    status: Status | None = None
    balance: float | None = None

    @field_validator("status")
    def validate_status(cls, value: Status) -> Status:
        """Validate Payment Profile Status."""

        if value not in [Status.ACTIVE, Status.INACTIVE, Status.DELETED]:
            raise PaymentProfileError("Invalid Status.")

        return value
