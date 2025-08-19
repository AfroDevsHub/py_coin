"""Accounts: Serialiser for Account Model."""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import validate_call
from sqlalchemy.orm import joinedload

from lib.interfaces.exceptions import AccountError
from lib.interfaces.user.accounts import CreateAccountData, UpdateAccountData
from models import ENGINE
from models.user.accounts import Account
from serialisers.serialiser import ISerialiser


class AccountSerialiser(ISerialiser):
    """Serialiser for the Account Model."""

    @validate_call
    def create(self, data: CreateAccountData) -> Account:
        """CRUD Operation: Create Account."""

        with Session(ENGINE) as session:
            account = Account(user_id=data.user_id)

            try:
                session.add(account)
                session.commit()
                session.refresh(account)
            except IntegrityError as exc:
                raise AccountError("Account Not Created.") from exc

            return account

    @validate_call
    def read(self, model_id: UUID) -> Account:
        """CRUD Operation: Read Account."""

        with Session(ENGINE) as session:
            account = (
                session.query(Account)
                .options(joinedload(Account.user_profiles))
                .options(joinedload(Account.settings_profile))
                .options(joinedload(Account.payment_profiles))
                .get(model_id)
            )

            if not account:
                raise AccountError("Account Not Found.")

            return account

    @validate_call
    def update(self, model_id: UUID, data: UpdateAccountData) -> Account:
        """CRUD Operation: Update Account."""

        with Session(ENGINE) as session:
            account = session.get(Account, model_id)

            if account is None:
                raise AccountError("Account Not Found.")
            
            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(account, key, value)

            try:
                session.add(account)
                session.commit()
                session.refresh(account)
            except IntegrityError as exc:
                raise AccountError("Account Not Updated.") from exc

            return account

    @validate_call
    def delete(self, model_id: UUID) -> str:
        """CRUD Operation: Delete Account."""

        with Session(ENGINE) as session:
            account = session.get(Account, model_id)

            if not account:
                raise AccountError("Account Not Found")

            try:
                session.delete(account)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Deleted.") from exc

            return f"Deleted: {model_id}"

    @validate_call
    def get_accounts_by_user_id(self, user_id: UUID) -> list[Account]:
        """Get Account by User ID."""

        with Session(ENGINE) as session:
            account = session.query(Account).filter(Account.user_id == user_id).all()

            if not account:
                return []

            return account
