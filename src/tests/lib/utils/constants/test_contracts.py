"""Constants: Testing Contract Constants Module."""

from pytest import mark

from lib.utils.constants.contracts import ContractStatus


@mark.parametrize(
    "data",
    list(ContractStatus),
)
def test_contract_status_enum(data: ContractStatus) -> None:
    """Testing Contract Status Enum."""

    assert isinstance(data.value, str)
