"""Logins: Serialiser for Login History Model."""

from datetime import datetime
from typing import Any
from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, validate_call
from lib.interfaces.exceptions import (
    LoginHistoryError,
)
from lib.utils.constants.users import Country, LoginMethod
from models import ENGINE
from models.warehouse.logins import LoginHistory
from serialisers.serialiser import BaseSerialiser


class UpdateLoginHistory(BaseModel):
    session_id: UUID | None = None
    login_location: Country | None = None
    login_device: str | None = None
    login_method: LoginMethod | None = None
    logged_in: bool | None = None
    logout_date: datetime | None = None
    authentication_token: str | None = None


class LoginHistorySerialiser(LoginHistory, BaseSerialiser):
    """Serialiser for the Login History Model."""

    @validate_call
    def get_login_history(self, login_id: UUID) -> dict[str, Any]:
        """CRUD Operation: Get Login History."""

        with Session(ENGINE) as session:
            query = select(LoginHistory).filter(
                cast(LoginHistory.login_id, uuid) == login_id
            )
            login_history = session.execute(query).scalar_one_or_none()

            if not login_history:
                raise LoginHistoryError("Login History Not Found.")

            return self.__get_model_data__(login_history)

    @validate_call
    def create_login_history(self, user_id: UUID) -> str:
        """CRUD Operation: Add Login History."""

        with Session(ENGINE) as session:
            self.user_id = user_id

            try:
                session.add(self)
                session.commit()
            except IntegrityError as exc:
                raise LoginHistoryError("Login History Not Created.") from exc

            return str(self)

    @validate_call
    def update_login_history(self, private_id: UUID, data: UpdateLoginHistory) -> str:
        """CRUD Operation: Update Login History."""

        with Session(ENGINE) as session:
            login_history = session.get(LoginHistory, private_id)

            if login_history is None:
                raise LoginHistoryError("Login History Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(login_history, key, value)

            try:
                session.add(login_history)
                session.commit()
            except IntegrityError as exc:
                raise LoginHistoryError("Login History not Updated.") from exc

            return str(login_history)

    @validate_call
    def delete_login_history(self, private_id: UUID) -> str:
        """CRUD Operation: Delete Login History."""

        with Session(ENGINE) as session:
            login_history = session.get(LoginHistory, private_id)

            if not login_history:
                raise LoginHistoryError("Login History Not Found")

            try:
                session.delete(login_history)
                session.commit()
            except IntegrityError as exc:
                raise LoginHistoryError("Login History not Deleted.") from exc

            return f"Deleted: {private_id}"
