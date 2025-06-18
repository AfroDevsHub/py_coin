"""Validators: Testing Transaction Module."""

from pytest import mark, raises
from lib.exceptions import TransactionError
from lib.utils.constants.transactions import TransactionStatus
from lib.validators.transactions import (
    validate_transaction_amount,
    validate_transaction_status,
)


@mark.parametrize(
    "amount",
    [5.0, 55.0, 1500.0],
)
def test_validate_transaction_amount(get_transactions, amount):
    """Tests Validating Transaction Amount."""

    draft_transaction = get_transactions[0]
    assert validate_transaction_amount(amount=amount, model=draft_transaction) == amount


@mark.parametrize(
    "amount",
    [5.0, 55.0, 1500.0],
)
def test_invalidate_transaction_amount_invalid(get_transactions, amount):
    """Tests Invalidating Transaction Amount."""

    for transaction in get_transactions[1:]:
        with raises(TransactionError):
            validate_transaction_amount(amount=amount, model=transaction)


@mark.parametrize(
    "amount",
    [-5.0, "55.0", 0.0, "Hello World", 5],
)
def test_invalidate_transaction_status(get_transactions, amount):
    """Tests Invalidating Transaction Amount."""

    for transaction in get_transactions[1:]:
        with raises(TransactionError):
            validate_transaction_amount(amount=amount, model=transaction)


@mark.parametrize(
    "status",
    [TransactionStatus.APPROVED, TransactionStatus.REJECTED],
)
def test_invalidate_draft_transaction_status(get_transactions, status):
    """Tests Invalidating Draft Transaction Status."""

    draft_transaction = get_transactions[0]
    assert validate_transaction_status(status, model=draft_transaction) == status


@mark.parametrize(
    "status",
    [TransactionStatus.TRANSFERED, TransactionStatus.INSUFFICIENT],
)
def test_validate_transferred_transaction_status(get_transactions, status):
    """Tests Validating Transferred Transaction Status."""

    approved_transaction = get_transactions[1]
    assert validate_transaction_status(status, model=approved_transaction) == status


@mark.parametrize(
    "status",
    [TransactionStatus.REVERSED],
)
def test_validate_reversed_transaction_status(get_transactions, status):
    """Tests Invalidating Reversed Transaction Status."""

    approved_transaction = get_transactions[2]
    assert validate_transaction_status(status, model=approved_transaction) == status


@mark.parametrize(
    "status",
    list(TransactionStatus),
)
def test_invalidate_approved_transaction_status(get_transactions, status):
    """Tests Invalidating Unapproved Transaction Status."""

    rejected_transaction = get_transactions[2]
    with raises(TransactionError):
        if status in [
            TransactionStatus.REVERSED,
            TransactionStatus.TRANSFERED,
        ]:
            raise TransactionError("Testing Transactions - Reversed Test.")
        assert validate_transaction_status(status, model=rejected_transaction) == status
