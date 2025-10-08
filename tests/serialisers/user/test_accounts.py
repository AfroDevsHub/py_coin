"""User: Testing Accounts Serialiser."""

<<<<<<< HEAD
from uuid import uuid4
from pydantic import ValidationError
=======
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from lib.exceptions import AccountError, UserError
from lib.types.user import AccountData
from lib.utils.constants.users import Status
from models.user.accounts import Account
from serialisers.user.accounts import AccountSerialiser
from models import ENGINE
from services.authentication import AbstractService
from conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


def test_accountprofileserialiser_create(get_users):
    """Testing Account Serialiser: Create Account."""

    for user in get_users:
        with Session(ENGINE) as session:
            account = AccountSerialiser().create_account(user.id)
            account_id = AbstractService.get_public_id(account)
            account = (
                session.query(Account)
                .filter(Account.account_id == account_id)
                .one_or_none()
            )
            assert account.id is not None

            run_test_teardown([account], session)


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_accountprofileserialiser_create_invalid(data):
    """Testing Account Serialiser: Create Account."""

    with raises((AccountError, DataError, ProgrammingError)):
        AccountSerialiser().create_account(data)


def test_accountprofileserialiser_get(get_accounts):
    """Testing Account Serialiser: Get Account."""

    for account in get_accounts:
        account_data = AccountSerialiser().get_account(account.account_id)

        assert isinstance(account_data, dict)
        for key in account_data:
            assert key not in Account.__EXCLUDE_ATTRIBUTES__


@mark.parametrize("data", check_invalid_ids())
def test_accountprofileserialiser_get_invalid(data):
    """Testing Account Serialiser: Get Account."""

    with raises((AccountError, DataError, ProgrammingError)):
        AccountSerialiser().get_account(data)


def test_accountprofileserialiser_delete(get_accounts):
    """Testing Account Serialiser: Delete Account."""

    for account in get_accounts:
        assert AccountSerialiser().delete_account(account.id).startswith("Deleted: ")


@mark.parametrize("data", check_invalid_ids())
def test_accountprofileserialiser_delete_invalid(data):
    """Testing Account Serialiser: Delete Account."""

    with raises((AccountError, ProgrammingError, DataError)):
        assert AccountSerialiser().delete_account(data).startswith("Deleted: ")


@mark.parametrize(
    "data",
    [
        Status.ACTIVE,
        Status.DELETED,
        Status.NEW,
    ],
)
def test_accountprofileserialiser_update_valid_status(get_accounts, data):
    """Testing Account Serialiser: Update Account."""

    for account in get_accounts:
        with Session(ENGINE) as session:
            AccountSerialiser().update_account(account.id, AccountData(status=data))
            account = session.get(Account, account.id)
            assert account.id is not None
            assert account.status == data


@mark.parametrize(
    "data",
    [Status.DISABLED, Status.INACTIVE, "Account ID.", None, 1],
)
def test_accountprofileserialiser_update_invalid_status(get_accounts, data):
    """Testing Account Serialiser: Update Account."""

    for account in get_accounts:
        with raises((UserError, AccountError, ValidationError)):
            AccountSerialiser().update_account(account.id, AccountData(status=data))
            if not isinstance(data, Status):
                AccountSerialiser().update_account(data)
