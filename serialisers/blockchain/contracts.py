"""Contracts: Serialiser for Contract Model."""

from typing import Any
from uuid import UUID
from pydantic import BaseModel, field_validator, validate_call
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from lib.interfaces.exceptions import ContractError
from lib.utils.constants.users import Status
from lib.utils.encryption.encoders import get_hash_value
from lib.validators.contracts import validate_contract_status
from models import ENGINE
from models.blockchain.contracts import Contract
from models.user.payments import PaymentProfile
from models.warehouse.cards import Card
from serialisers.serialiser import BaseSerialiser


class UpdateContractData(BaseModel):
    title: str | None = None
    description: str | None = None
    contract_status: Status | None = None


class ContractSerialiser(Contract, BaseSerialiser):
    """Serialiser for the Contract Model."""

    __SERIALISER_EXCEPTION__ = ContractError

    @validate_call
    def get_contract(self, contract_id: str) -> dict[str, Any]:
        """CRUD Operation: Read Contract."""

        with Session(ENGINE) as session:
            query = select(Contract).filter(
                cast(Contract.contract_id, String) == contract_id
            )
            contract = session.execute(query).scalar_one_or_none()

            if not contract:
                raise ContractError("Contract Not Found.")

            return self.__get_model_data__(contract)

    @validate_call
    def create_contract(self, contractor: UUID, contractee: UUID, contract: str) -> str:
        """CRUD Operation: Create Contract."""

        with Session(ENGINE) as session:
            contractor_profile = session.get(PaymentProfile, contractor)
            contractee_profile = session.get(PaymentProfile, contractee)
            if not contractor_profile:
                raise ContractError("Invalid Sender.")
            if not contractee_profile:
                raise ContractError("Invalid Receiver.")

            self.contract_id = get_hash_value(contract, str(self.salt_value))
            self.contractor = contractor
            self.contractee = contractee
            self.contract = contract

            contractor_card = session.get(Card, contractor_profile.card_id)
            contractee_card = session.get(Card, contractee_profile.card_id)

            if not contractor_card:
                raise ContractError("Invalid Sender Card Information.")
            if not contractee_card:
                raise ContractError("Invalid Receiver Card Information.")

            self.contractor_signiture = get_hash_value(
                str(contractor_card.card_id),
                str(self.salt_value),
            )
            self.contractee_signiture = get_hash_value(
                str(contractee_card.card_id),
                str(self.salt_value),
            )

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise ContractError("Contract Not Created.") from exc

            return str(self)

    @validate_call
    def update_contract(
        self,
        private_id: str,
        contractor_signiture: str,
        contractee_signiture: str,
        data: UpdateContractData,
    ) -> str:
        """CRUD Operation: Update Contract."""

        with Session(ENGINE) as session:
            contract = session.get(Contract, private_id)

            if contract is None:
                raise ContractError("Contract Not Found.")

            if str(contract.contractor_signiture) != contractor_signiture:
                raise ContractError("Sender Not Authorised.")
            if str(contract.contractee_signiture) != contractee_signiture:
                raise ContractError("Receiver Not Authorised.")

            for key, value in data.model_dump().items():
                if value is not None and key == "contract_status":
                    contract.contract_status = validate_contract_status(value, contract)

            try:
                session.add(contract)
                session.commit()
            except IntegrityError as exc:
                raise ContractError("Contract Not Updated.") from exc

            return str(Contract)

    @validate_call
    def delete_contract(self, private_id: UUID) -> str:
        """CRUD Operation: Delete Contract."""

        with Session(ENGINE) as session:
            contract = session.get(Contract, private_id)

            if not contract:
                raise ContractError("Contract Not Found")

            try:
                session.delete(contract)
                session.commit()
            except IntegrityError as exc:
                raise ContractError("Contract Not Deleted.") from exc

            return f"Deleted: {private_id}"
