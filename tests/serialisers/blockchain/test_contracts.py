"""BlockChain: Testing Contract Serialiser."""

from base64 import b64encode
from pytest import mark, raises
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, ProgrammingError

from lib.exceptions import ContractError
from lib.utils.constants.contracts import ContractStatus
from lib.utils.encryption.cryptography import encrypt_data
from models.blockchain.contracts import Contract
from serialisers.blockchain.contracts import ContractSerialiser
from models import ENGINE
from services.authentication import AbstractService
from conftest import run_test_teardown
from tests.test_utils.utils import check_invalid_ids


def __read_file__():
    """Util Function to Read the sample File."""
    with open("tests/test_contract.html", "rb") as file:
        return b64encode(file.read())


@mark.parametrize(
    "data",
    [
        encrypt_data("Test Contract Data String.".encode()),
        encrypt_data("Any Valid Test String".encode()),
        encrypt_data(__read_file__()),
    ],
)
def test_contractserialiser_create(get_payments, data):
    """Testing Contract Serialiser: Create Contract."""

    for payment, payment1 in zip(get_payments, list(reversed(get_payments))):
        with Session(ENGINE) as session:
            contract = ContractSerialiser().create_contract(
                payment.id, payment1.id, data
            )
            contract_id = AbstractService.get_public_id(contract)
            contract = (
                session.query(Contract)
                .filter(Contract.contract_id == contract_id)
                .one_or_none()
            )
            assert contract.id is not None
            assert contract.contract == data

            run_test_teardown([contract], session)


@mark.parametrize(
    "data",
    zip(check_invalid_ids(), list(reversed(check_invalid_ids())), (-50, "500", 0.0)),
)
def test_contracter_create_invalid(data):
    """Testing Contract Serialiser: Create Contract."""

    with raises((ContractError, DataError, ProgrammingError)):
        ContractSerialiser().create_contract(data[0], data[1], data[1])


def test_contractileserialiser_get(get_contracts):
    """Testing Contract Serialiser: Get Contract."""

    for contract in get_contracts:
        contract_data = ContractSerialiser().get_contract(contract.contract_id)

        assert isinstance(contract_data, dict)
        for key in contract_data:
            assert key not in contract.__EXCLUDE_ATTRIBUTES__


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_contractliser_get_invalid(data):
    """Testing Contract Serialiser: Get Contract."""

    with raises((ContractError, DataError, ProgrammingError)):
        ContractSerialiser().get_contract(data)


def test_contractserialiser_delete(get_contracts):
    """Testing Contract Serialiser: Delete Contract."""

    for contract in get_contracts:
        assert ContractSerialiser().delete_contract(contract.id).startswith("Deleted: ")


@mark.parametrize(
    "data",
    check_invalid_ids(),
)
def test_contracter_delete_invalid(data):
    """Testing Contract Serialiser: Delete Contract."""

    with raises((ContractError, DataError, ProgrammingError)):
        ContractSerialiser().delete_contract(data)


@mark.parametrize(
    "data",
    [
        {
            "title": "Test Contract Data String",
            "description": "Any Valid Test String",
        },
        {
            "title": "Test Contract Data String",
            "description": "Any Valid Test String",
        },
    ],
)
def test_contract_update_valid_contract(get_contracts, data):
    """Testing Contract Serialiser: Update Contract."""

    for contract in get_contracts:
        with Session(ENGINE) as session:
            ContractSerialiser().update_contract(
                contract.id,
                contract.contractor_signiture,
                contract.contractee_signiture,
                **data,
            )
            contract = session.get(Contract, contract.id)
            assert contract.id is not None
            for key, value in data.items():
                assert getattr(contract, key) == value


@mark.parametrize(
    "data",
    [
        {
            "title": 1,
            "description": 1,
        },
        {
            "title": "Test",
            "description": "Any",
        },
        {
            "title": "   ",
            "description": "   ",
        },
    ],
)
def test_contract_update_invalid_contract(get_contracts, data):
    """Testing Contract Serialiser: Update Contract."""

    for contract in get_contracts:
        with raises((ContractError, DataError, ProgrammingError)):
            ContractSerialiser().update_contract(
                contract.id,
                contract.contractor_signiture,
                contract.contractee_signiture,
                contract=data,
            )


@mark.parametrize(
    "data",
    [
        {
            "draft": ContractStatus.APPROVED,
            "approved": ContractStatus.CLOSED,
            "closed": ContractStatus.CLOSED,
        },
        {
            "draft": ContractStatus.REJECTED,
            "approved": ContractStatus.ACTIVE,
            "closed": ContractStatus.CLOSED,
        },
    ],
)
def test_contractte_valid_status_app(get_contracts, data):
    """Testing Contract Serialiser: Update Contract."""

    with Session(ENGINE) as session:
        for contract in get_contracts:
            match (contract.contract_status):
                case ContractStatus.DRAFT:
                    contract_status = data.get("draft")
                case ContractStatus.APPROVED:
                    contract_status = data.get("approved")
                case ContractStatus.CLOSED:
                    contract_status = data.get("closed")
                case _:
                    continue
            ContractSerialiser().update_contract(
                contract.id,
                contract.contractor_signiture,
                contract.contractee_signiture,
                contract_status=contract_status,
            )
            contract_data = session.get(Contract, contract.id)
            assert contract_data.id is not None
            assert contract_data.contract_status == contract_status


@mark.parametrize(
    "data",
    [
        {
            "draft": ContractStatus.CLOSED,
        },
        {
            "closed": ContractStatus.APPROVED,
        },
        {
            "draft": ContractStatus.ACTIVE,
            "closed": ContractStatus.ACTIVE,
        },
        {
            "approved": ContractStatus.REJECTED,
            "closed": ContractStatus.REJECTED,
        },
    ],
)
def test_contractte_invalid_status_app(get_contracts, data):
    """Testing Contract Serialiser: Update Contract."""

    for contract in get_contracts:
        match (contract.contract_status):
            case ContractStatus.DRAFT:
                contract_status = data.get("draft")
            case ContractStatus.APPROVED:
                contract_status = data.get("approved")
            case ContractStatus.CLOSED:
                contract_status = data.get("closed")
            case _:
                contract_status = None
        with raises((ContractError, DataError, ProgrammingError)):
            ContractSerialiser().update_contract(
                contract.id,
                contract.contractor_signiture,
                contract.contractee_signiture,
                contract_status=contract_status,
            )
