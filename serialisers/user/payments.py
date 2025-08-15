"""Payments: Serialiser for Payment Profile Model."""

from typing import Any
from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, field_validator, validate_call
from lib.interfaces.exceptions import PaymentProfileError
from lib.utils.constants.users import Status
from models import ENGINE
from models.user.payments import PaymentProfile
from serialisers.serialiser import BaseSerialiser


class UpdatePaymentProfile(BaseModel):
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


class PaymentProfileSerialiser(PaymentProfile, BaseSerialiser):
    """Serialiser for the Payment Profile Model."""

    @validate_call
    def get_payment_profile(self, payment_id: UUID) -> dict[str, Any]:
        """CRUD Operation: Get Payment Profile."""

        with Session(ENGINE) as session:
            query = select(PaymentProfile).filter(
                cast(PaymentProfile.payment_id, uuid) == payment_id
            )
            payment_profile = session.execute(query).scalar_one_or_none()

            if not payment_profile:
                raise PaymentProfileError("Payment Profile not Found.")

            return self.__get_model_data__(payment_profile)

    @validate_call
    def create_payment_profile(self, account_id: UUID, card_id: UUID) -> str:
        """CRUD Operation: Add Payment Profile."""

        with Session(ENGINE) as session:
            self.card_id = card_id
            self.account_id = account_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Created.") from exc

            return str(self)

    @validate_call
    def update_payment_profile(self, private_id: str, data: UpdatePaymentProfile) -> str:
        """CRUD Operation: Update Payment Profile."""

        with Session(ENGINE) as session:
            payment_profile = session.get(PaymentProfile, private_id)

            if payment_profile is None:
                raise PaymentProfileError("Payment Profile Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(payment_profile, key, value)

            try:
                session.add(payment_profile)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Updated.") from exc

            return str(payment_profile)

    @validate_call
    def delete_payment_profile(self, private_id: UUID) -> str:
        """CRUD Operation: Delete Payment Profile."""

        with Session(ENGINE) as session:
            payment_profile = session.get(PaymentProfile, private_id)

            if not payment_profile:
                raise PaymentProfileError("Payment Profile Not Found")

            try:
                session.delete(payment_profile)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Deleted.") from exc

            return f"Deleted: {private_id}"
