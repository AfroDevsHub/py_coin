"""Logins: Serialiser for Login History Model."""

from uuid import UUID
from sqlalchemy import cast, select, UUID as uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from lib.exceptions import (
    LoginHistoryError,
)
from models import ENGINE
from models.warehouse.logins import LoginHistory
from serialisers.serialiser import BaseSerialiser


class LoginHistorySerialiser(LoginHistory, BaseSerialiser):
    """Serialiser for the Login History Model."""

    __SERIALISER_EXCEPTION__ = LoginHistoryError
    __MUTABLE_KWARGS__: list[str] = [
        "session_id",
        "login_location",
        "login_device",
        "login_method",
        "logged_in",
        "logout_date",
        "authentication_token",
    ]

    def get_login_history(self, login_id: UUID) -> dict:
        """CRUD Operation: Get Login History."""

        with Session(ENGINE) as session:
            query = select(LoginHistory).filter(cast(LoginHistory.login_id, uuid) == login_id)
            login_history = session.execute(query).scalar_one_or_none()

            if not login_history:
                raise LoginHistoryError("Login History Not Found.")

            return self.__get_model_data__(login_history)

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

    def update_login_history(self, private_id: UUID, **kwargs) -> str:
        """CRUD Operation: Update Login History."""

        with Session(ENGINE) as session:
            login_history = session.get(LoginHistory, private_id)

            if login_history is None:
                raise LoginHistoryError("Login History Not Found.")

            for key, value in kwargs.items():
                if key not in LoginHistorySerialiser.__MUTABLE_KWARGS__:
                    raise LoginHistoryError("Invalid Login History.")

                value = self.validate_serialiser_kwargs(key, value)
                setattr(login_history, key, value)
            try:
                session.add(login_history)
                session.commit()
            except IntegrityError as exc:
                raise LoginHistoryError("Login History not Updated.") from exc

            return str(login_history)

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
