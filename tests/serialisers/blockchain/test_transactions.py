"""BlockChain: Testing Transaction Serialiser."""

from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from lib.exceptions import TransactionError
from lib.utils.constants.transactions import TransactionStatus
from models.blockchain.transactions import Transaction
from serialisers.blockchain.transactions import TransactionSerialiser
from models import ENGINE
from services.authentication import AbstractService
from conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


@mark.parametrize("data", [50.0, 55.5, 1234656.02])
def test_transactionserialiser_create(get_payments, data):
    """Testing transaction Serialiser: Create transaction."""

    for payment, payment1 in zip(get_payments, list(reversed(get_payments))):
        with Session(ENGINE) as session:
            transaction = TransactionSerialiser().create_transaction(
                payment.id, payment1.id, data
            )
            transaction_id = AbstractService.get_public_id(transaction)
            transaction = (
                session.query(Transaction)
                .filter(Transaction.transaction_id == transaction_id)
                .one_or_none()
            )
            assert transaction.id is not None
            assert transaction.amount == data

            run_test_teardown([transaction], session)


@mark.parametrize(
    "data",
    zip(check_invalid_ids(), list(reversed(check_invalid_ids())), (-50, "500", 0.0)),
)
def test_transactioner_create_invalid(data):
    """Testing transaction Serialiser: Create transaction."""

    with raises((TransactionError, DataError, ProgrammingError)):
        TransactionSerialiser().create_transaction(data[0], data[1], data[1])


def test_transactionileserialiser_get(get_transactions):
    """Testing transaction Serialiser: Get transaction."""

    for transaction in get_transactions:
        transaction_data = TransactionSerialiser().get_transaction(
            transaction.transaction_id
        )

        assert isinstance(transaction_data, dict)
        for key in transaction_data:
            assert key not in transaction.__EXCLUDE_ATTRIBUTES__


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_transactionliser_get_invalid(data):
    """Testing transaction Serialiser: Get transaction."""

    with raises((TransactionError, DataError, ProgrammingError)):
        TransactionSerialiser().get_transaction(data)


def test_transactionserialiser_delete(get_transactions):
    """Testing transaction Serialiser: Delete transaction."""

    for transaction in get_transactions:
        assert (
            TransactionSerialiser()
            .delete_transaction(transaction.id)
            .startswith("Deleted: ")
        )


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_transactioner_delete_invalid(data):
    """Testing transaction Serialiser: Delete transaction."""

    with raises((TransactionError, DataError, ProgrammingError)):
        TransactionSerialiser().delete_transaction(data)


@mark.parametrize(
    "data",
    [55.0, 4505775.7, 0.1],
)
def test_transaction_update_valid_amount(get_transactions, data):
    """Testing transaction Serialiser: Update transaction."""

    for transaction in get_transactions:
        if transaction.transaction_status != TransactionStatus.DRAFT:
            continue
        with Session(ENGINE) as session:
            TransactionSerialiser().update_transaction(
                transaction.id,
                transaction.sender_signiture,
                transaction.receiver_signiture,
                amount=data,
            )
            transaction = session.get(Transaction, transaction.id)
            assert transaction.id is not None
            assert transaction.amount == data
            assert transaction.transaction_status == TransactionStatus.DRAFT


@mark.parametrize(
    "data",
    [-55.0, 0.0, "0.1"],
)
def test_transaction_update_invalid_amount(get_transactions, data):
    """Testing transaction Serialiser: Update transaction."""

    for transaction in get_transactions:
        with raises((TransactionError, DataError, ProgrammingError)):
            TransactionSerialiser().update_transaction(
                transaction.id,
                transaction.sender_signiture,
                transaction.receiver_signiture,
                amount=data,
            )


@mark.parametrize(
    "data",
    [
        {
            "draft": TransactionStatus.APPROVED,
            "approved": TransactionStatus.TRANSFERED,
            "transferred": TransactionStatus.REVERSED,
        },
        {
            "draft": TransactionStatus.REJECTED,
            "approved": TransactionStatus.INSUFFICIENT,
            "transferred": TransactionStatus.REVERSED,
        },
    ],
)
def test_transactionte_valid_status_app(get_transactions, data):
    """Testing transaction Serialiser: Update transaction."""

    with Session(ENGINE) as session:
        for transaction in get_transactions:
            match (transaction.transaction_status):
                case TransactionStatus.DRAFT:
                    transaction_status = data.get("draft")
                case TransactionStatus.APPROVED:
                    transaction_status = data.get("approved")
                case TransactionStatus.TRANSFERED:
                    transaction_status = data.get("transferred")
                case _:
                    transaction_status = None
            TransactionSerialiser().update_transaction(
                transaction.id,
                transaction.sender_signiture,
                transaction.receiver_signiture,
                transaction_status=transaction_status,
            )
            transaction = session.get(Transaction, transaction.id)
            assert transaction.id is not None
            assert transaction.transaction_status == transaction_status


@mark.parametrize(
    "data",
    [
        {
            "draft": TransactionStatus.TRANSFERED,
        },
        {
            "transferred": TransactionStatus.APPROVED,
        },
        {
            "draft": TransactionStatus.INSUFFICIENT,
            "transferred": TransactionStatus.INSUFFICIENT,
        },
        {
            "approved": TransactionStatus.REJECTED,
            "transferred": TransactionStatus.REJECTED,
        },
        {
            "draft": TransactionStatus.REVERSED,
            "approved": TransactionStatus.REVERSED,
        },
    ],
)
def test_transactionte_invalid_status_app(get_transactions, data):
    """Testing transaction Serialiser: Update transaction."""

    for transaction in get_transactions:
        match (transaction.transaction_status):
            case TransactionStatus.DRAFT:
                transaction_status = data.get("draft")
            case TransactionStatus.APPROVED:
                transaction_status = data.get("approved")
            case TransactionStatus.TRANSFERED:
                transaction_status = data.get("transferred")
            case _:
                transaction_status = None
        with raises((TransactionError, DataError, ProgrammingError)):
            TransactionSerialiser().update_transaction(
                transaction.id,
                transaction.sender_signiture,
                transaction.receiver_signiture,
                transaction_status=transaction_status,
            )
