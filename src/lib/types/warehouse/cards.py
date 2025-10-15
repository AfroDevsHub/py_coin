from pydantic import BaseModel, field_validator
from src.lib.types.exceptions import CardValidationError
from src.lib.utils.constants.users import CardType, Regex, Status


class CreateCardData(BaseModel):
    card_type: CardType
    pin: str

    @field_validator("pin")
    def validate_pin(cls, value: str) -> str:
        if not Regex.PIN.value.match(value):
            raise CardValidationError("Invalid Pin")

        return value


class UpdateCardData(BaseModel):
    status: Status | None = None
    pin: str | None = None

    @field_validator("pin")
    def validate_pin(cls, value: str) -> str:
        if not Regex.PIN.value.match(value):
            raise CardValidationError("Invalid Pin")

        return value

    @field_validator("status")
    def validate_status(cls, value: Status) -> Status:
        """Validate Account Status."""

        if value not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
            raise CardValidationError("Invalid Status.")

        return value
