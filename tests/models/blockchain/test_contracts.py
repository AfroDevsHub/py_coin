"""BlockChain: Testing Contract Model."""

from pytest import raises

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.utils.constants.contracts import ContractStatus
from lib.utils.encryption.cryptography import encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from models import ENGINE
from models.blockchain.contracts import Contract
from models.user.payments import PaymentProfile
from conftest import run_test_teardown


def test_contract_invalid_no_args() -> None:
    """Testing Contract With Missing Attributes."""

    with Session(ENGINE) as session:
        with raises(IntegrityError):
            contract = Contract()
            session.add(contract)
            session.commit()


def test_contract_invalid_args() -> None:
    """Testing Constructor, for Invalid Arguments."""

    with Session(ENGINE) as session:
        with raises(TypeError):
            contract = Contract("email", "password")  # type: ignore
            session.add(contract)
            session.commit()


def test_contract_valid(get_payments: list[PaymentProfile]) -> None:
    """Testing a Valid Contract Constructor, with Required Arguments."""

    for contractor, contractee in zip(get_payments, list(reversed(get_payments))):
        with Session(ENGINE) as session:
            with open("test_markdown.md", "r", encoding="utf-8") as file:
                contract = Contract()
                contract.contract_id = get_hash_value(
                    file.read(), str(contract.salt_value)
                )
                contract.contractor = contractor.id
                contract.contractee = contractee.id
                contract.contract = encrypt_data(file.read().encode())
                session.add(contract)
                session.commit()

                assert contract.id is not None
                assert contract.contract_status == ContractStatus.DRAFT
                assert isinstance(contract.to_dict(), dict)

                run_test_teardown([contract], session)
