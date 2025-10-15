"""Logins: Serialiser for Login History Model."""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import validate_call
from src.models import ENGINE
from src.models.warehouse.logins import LoginHistory
from src.serialisers.serialiser import ISerialiser
from src.lib.types.exceptions import LoginHistoryError
from src.lib.types.warehouse.login_history import CreateLoginHistory, UpdateLoginHistory


class LoginHistorySerialiser(ISerialiser):
    """Serialiser for the Login History Model."""

    @validate_call
    def create(self, data: CreateLoginHistory) -> LoginHistory:
        """CRUD Operation: Add Login History."""

        with Session(ENGINE) as session:
            login_history = LoginHistory(user_id=data.user_id)

            try:
                session.add(login_history)
                session.commit()
                session.refresh(login_history)
            except IntegrityError as exc:
                raise LoginHistoryError("Login History Not Created.") from exc

            return login_history

    @validate_call
    def read(self, model_id: UUID) -> LoginHistory:
        """CRUD Operation: Get Login History."""

        with Session(ENGINE) as session:
            login_history = session.get(LoginHistory, model_id)

            if not login_history:
                raise LoginHistoryError("Login History Not Found.")

            return login_history

    @validate_call
    def update(self, model_id: UUID, data: UpdateLoginHistory) -> LoginHistory:
        """CRUD Operation: Update Login History."""

        with Session(ENGINE) as session:
            login_history = session.get(LoginHistory, model_id)

            if login_history is None:
                raise LoginHistoryError("Login History Not Found.")

            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(login_history, key, value)

            try:
                session.add(login_history)
                session.commit()
                session.refresh(login_history)
            except IntegrityError as exc:
                raise LoginHistoryError("Login History not Updated.") from exc

            return login_history

    @validate_call
    def delete(self, model_id: UUID) -> str:
        """CRUD Operation: Delete Login History."""

        with Session(ENGINE) as session:
            login_history = session.get(LoginHistory, model_id)

            if not login_history:
                raise LoginHistoryError("Login History Not Found")

            try:
                session.delete(login_history)
                session.commit()
            except IntegrityError as exc:
                raise LoginHistoryError("Login History not Deleted.") from exc

            return f"Deleted: {model_id}"
