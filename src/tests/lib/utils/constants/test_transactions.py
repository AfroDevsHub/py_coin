"""Constants: Testing Transaction Constants Module."""

from pytest import mark

from lib.utils.constants.transactions import TransactionStatus


@mark.parametrize(
    "data",
    list(TransactionStatus),
)
def test_transaction_status_enum(data: TransactionStatus) -> None:
    """Testing Transaction Statuss Enum."""

    assert isinstance(data.value, str)
