"""Contracts: validations for Contract Related Models."""

from lib.exceptions import ContractError
from lib.utils.constants.contracts import ContractStatus
from models.blockchain.contracts import Contract

def validate_contract_status(
    status: ContractStatus, **kwargs
) -> ContractStatus:
    """Validates Contract Amount."""

    contract = kwargs.get("model")
    if not isinstance(contract, Contract):
        raise ContractError("Invalid Type for this Attribute.")
    if not isinstance(status, ContractStatus):
        raise ContractError("Invalid Type for this Attribute.")
    if contract.contract_status == status:
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
        case None:
            return ContractStatus.DRAFT
        case _:
            raise ContractError("Invalid Contract Status.")
    raise ContractError("Invalid Contract Status.")
    