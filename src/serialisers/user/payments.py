"""Payments: Serialiser for Payment Profile Model."""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
<<<<<<< HEAD
from lib.exceptions import PaymentProfileError
=======
from pydantic import validate_call
from lib.interfaces.exceptions import PaymentProfileError
from lib.interfaces.user.payments import (
    CreatePaymentProfileData,
    UpdatePaymentProfileData,
)
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from models import ENGINE
from models.user.payments import PaymentProfile
from serialisers.serialiser import ISerialiser


class PaymentProfileSerialiser(ISerialiser):
    """Serialiser for the Payment Profile Model."""

<<<<<<< HEAD
    __SERIALISER_EXCEPTION__ = PaymentProfileError
    __MUTABLE_KWARGS__: list[str] = [
        "name",
        "description",
        "status",
        "balance",
    ]

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

    def create_payment_profile(self, account_id: UUID, card_id: UUID) -> str:
=======
    @validate_call
    def create(self, data: CreatePaymentProfileData) -> PaymentProfile:
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
        """CRUD Operation: Add Payment Profile."""

        with Session(ENGINE) as session:
            print(f"Creating Payment Profile: Account ID: {data.account_id} | Card ID: {data.card_id}")
            payment_profile = PaymentProfile(
                account_id=data.account_id, card_id=data.card_id
            )

            try:
                session.add(payment_profile)
                session.commit()
                session.refresh(payment_profile)
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Created.") from exc

            return payment_profile

    @validate_call
    def read(self, model_id: UUID) -> PaymentProfile:
        """CRUD Operation: Get Payment Profile."""

        with Session(ENGINE) as session:
            payment_profile = session.get(PaymentProfile, model_id)

            if not payment_profile:
                raise PaymentProfileError("Payment Profile not Found.")

            return payment_profile

    @validate_call
    def update(self, model_id: UUID, data: UpdatePaymentProfileData) -> PaymentProfile:
        """CRUD Operation: Update Payment Profile."""

        with Session(ENGINE) as session:
            payment_profile = session.get(PaymentProfile, model_id)

            if payment_profile is None:
                raise PaymentProfileError("Payment Profile Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(payment_profile, key, value)

            try:
                session.add(payment_profile)
                session.commit()
                session.refresh(payment_profile)
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Updated.") from exc

            return payment_profile

    @validate_call
    def delete(self, model_id: UUID) -> str:
        """CRUD Operation: Delete Payment Profile."""

        with Session(ENGINE) as session:
            payment_profile = session.get(PaymentProfile, model_id)

            if not payment_profile:
                raise PaymentProfileError("Payment Profile Not Found")

            try:
                session.delete(payment_profile)
                session.commit()
            except IntegrityError as exc:
                raise PaymentProfileError("Payment Profile not Deleted.") from exc

            return f"Deleted: {model_id}"
