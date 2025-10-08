"""Validators: Testing Contracts Module."""

from pytest import mark, raises
from lib.exceptions import ContractError
from lib.utils.constants.contracts import ContractStatus
from lib.validators.contracts import validate_contract_status
from models.blockchain.contracts import Contract


@mark.parametrize(
    "status",
    [ContractStatus.APPROVED, ContractStatus.REJECTED],
)
def test_validate_draft_contract_status(get_contracts: Contract, status: ContractStatus) -> None:
    """Tests Validating Draft Contract Status."""

    draft_contract = get_contracts[0]
    assert validate_contract_status(status, model=draft_contract) == status


@mark.parametrize(
    "status",
    [ContractStatus.ACTIVE, ContractStatus.CLOSED],
)
def test_validate_approved_contract_status(get_contracts: Contract, status: ContractStatus) -> None:
    """Tests Validating Approved Contract Status."""

    approved_contract = get_contracts[1]
    assert validate_contract_status(status, model=approved_contract) == status


@mark.parametrize(
    "status",
    list(ContractStatus),
)
def test_invalidate_rejected_contract_status(get_contracts: Contract, status: ContractStatus) -> None:
    """Tests Invalidating Unapproved Contract Status."""

    rejected_contract = get_contracts[2]
    with raises(ContractError):
        if get_contracts[2].contract_status != status:
            validate_contract_status(status, model=rejected_contract)
        else:
            raise ContractError("Invalid COntract")
