"""Accounts: Serialiser for Account Model."""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import validate_call
from sqlalchemy.orm import joinedload

<<<<<<< HEAD
from lib.exceptions import AccountError
from lib.types.user import AccountData
=======
from lib.interfaces.exceptions import AccountError
from lib.interfaces.user.accounts import CreateAccountData, UpdateAccountData
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from models import ENGINE
from models.user.accounts import Account
from serialisers.serialiser import ISerialiser


class AccountSerialiser(ISerialiser):
    """Serialiser for the Account Model."""

<<<<<<< HEAD
    __SERIALISER_EXCEPTION__ = AccountError

    def get_account(self, account_id: UUID) -> dict[str, Any]:
        """CRUD Operation: Read Account."""

        with Session(ENGINE) as session:
            query = select(Account).filter(cast(Account.account_id, uuid) == account_id)
            account = session.execute(query).scalar_one_or_none()

            if not account:
                raise AccountError("Account Not Found.")

            return self.__get_model_data__(account)

    def create_account(self, user_id: UUID) -> str:
        """CRUD Operation: Create Account."""

        with Session(ENGINE) as session:
            self.user_id = user_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise AccountError("Account Not Created.") from exc

            return str(self)

    def update_account(self, private_id: UUID, data: AccountData) -> str:
        """CRUD Operation: Update Account."""

        with Session(ENGINE) as session:
            account = session.get(Account, private_id)

            if account is None:
                raise AccountError("Account Not Found.")

            for key, value in data.model_dump().items():
                setattr(account, key, value)
=======
    @validate_call
    def create(self, data: CreateAccountData) -> Account:
        """CRUD Operation: Create Account."""

        with Session(ENGINE) as session:
            account = Account(user_id=data.user_id)
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9

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
