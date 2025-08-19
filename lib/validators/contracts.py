"""Contracts: validations for Contract Related Models."""

from lib.interfaces.exceptions import ContractError
from lib.utils.constants.contracts import ContractStatus
from models.blockchain.contracts import Contract


def validate_contract_status(
    status: ContractStatus, contract: Contract
) -> ContractStatus:
    """Validates Contract Amount."""

    if ContractStatus(contract.contract_status) == status:
        return status

    match (contract.contract_status):
        case ContractStatus.DRAFT:
            if status in [
                ContractStatus.APPROVED,
                ContractStatus.REJECTED,
            ]:
                return status
        case ContractStatus.APPROVED:
            if status in [
                ContractStatus.ACTIVE,
                ContractStatus.CLOSED,
            ]:
                return status
        case ContractStatus.ACTIVE:
            if status == ContractStatus.CLOSED:
                return status
        case _:
            raise ContractError("Invalid Contract Status.")
    raise ContractError("Invalid Contract Status.")
