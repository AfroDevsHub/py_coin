"""Accounts: Serialiser for Account Model."""

from typing import Any
from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, field_validator, validate_call

from lib.interfaces.exceptions import AccountError
from lib.utils.constants.users import Status
from models import ENGINE
from models.user.accounts import Account
from serialisers.serialiser import BaseSerialiser

class UpdateAccount(BaseModel):
    """Data Model for Account Update."""

    status: Status

    @field_validator("status")
    def validate_status(cls, value: Status) -> Status:
        """Validate Account Status."""

        if value not in [Status.NEW, Status.ACTIVE, Status.DELETED]:
            raise AccountError("Invalid Status.")

        return value

class AccountSerialiser(Account, BaseSerialiser):
    """Serialiser for the Account Model."""

    @validate_call
    def get_account(self, account_id: str) -> dict[str, Any]:
        """CRUD Operation: Read Account."""

        with Session(ENGINE) as session:
            query = select(Account).filter(cast(Account.account_id, uuid) == account_id)
            account = session.execute(query).scalar_one_or_none()

            if not account:
                raise AccountError("Account Not Found.")

            return self.__get_model_data__(account)

    @validate_call
    def create_account(self, user_id: str) -> str:
        """CRUD Operation: Create Account."""

        with Session(ENGINE) as session:
            self.user_id = user_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Created.") from exc

            return str(self)

    @validate_call
    def update_account(self, private_id: str, data: UpdateAccount) -> str:
        """CRUD Operation: Update Account."""

        with Session(ENGINE) as session:
            account = session.get(Account, private_id)

            if account is None:
                raise AccountError("Account Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(account, key, value)

            try:
                session.add(account)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Updated.") from exc

            return str(account)

    @validate_call
    def delete_account(self, private_id: UUID) -> str:
        """CRUD Operation: Delete Account."""

        with Session(ENGINE) as session:
            account = session.get(Account, private_id)

            if not account:
                raise AccountError("Account Not Found")

            try:
                session.delete(account)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Deleted.") from exc

            return f"Deleted: {private_id}"
