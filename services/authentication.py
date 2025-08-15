"""Authentication: User Authentication Services."""

from datetime import datetime, timedelta
from json import dumps, loads
from os import getenv
from typing import Any, Callable
from uuid import UUID, uuid4
import jwt

from pydantic import BaseModel

from config import AppConfig
from lib.interfaces.data_classes import UserData
from lib.interfaces.responses import ServiceResponse
from lib.utils.constants.responses import ServiceStatus
from lib.utils.constants.users import Country, DateFormat, LoginMethod
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from lib.utils.helpers.users import generate_jwt_token, get_public_uuid
from serialisers.user.users import CreateUserData, UserSerialiser
from serialisers.warehouse.logins import LoginHistorySerialiser, UpdateLoginHistory

def handle_service_errors(func: Callable[..., Any]) -> Callable[..., ServiceResponse]:
    """Handles Service Errors."""

    def wrapper(*args: Any, **kwargs: Any) -> ServiceResponse:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            return ServiceResponse(
                message=str(exc),
                status=ServiceStatus.ERROR,
            )

    return wrapper

class LoginData(BaseModel):
    login_location: Country | None = None
    login_device: str | None = None
    login_method: LoginMethod | None = None


class AuthenticationService:
    """Manages Authentication Operations."""

    __instance = None
    ACTIVE = True

    def __new__(cls, *args: Any, **kwargs: Any) -> "AuthenticationService":
        """Singleton Class Constructor."""

        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    @handle_service_errors
    def register_user(self, email: str, password: str) -> ServiceResponse:
        """Registers User."""

        user_data = CreateUserData(email=email, password=password)
        response = UserSerialiser().create_user(user_data)
        public_id = get_public_uuid(response)
        return ServiceResponse(
            message=response, status=ServiceStatus.SUCCESS, data={"id": public_id}
        )

    @handle_service_errors
    def login_user(
        self, email: str, password: str, meta_data: LoginData
    ) -> ServiceResponse:
        """Logs a User In."""

        user_id = get_hash_value(email + password, str(AppConfig().salt_value))
        encrypted_user = UserSerialiser().get_user(user_id)
        user = loads(decrypt_data(encrypted_user))

        if isinstance(user.get("login_history", ""), list):
            for login in user["login_history"]:
                self.logout_user(loads(decrypt_data(login))["id"])

        response = LoginHistorySerialiser().create_login_history(user["id"])
        login_id = get_public_uuid(response)
        login_history = LoginHistorySerialiser().get_login_history(UUID(login_id))

        session_id = uuid4()
        token = generate_jwt_token(
            user_id=user["user_id"],
            login_id=login_history["login_id"],
            session_id=str(session_id),
            email=decrypt_data(user["email"]),
        )
        login_data = UpdateLoginHistory(
            session_id=session_id,
            login_location=meta_data.login_location,
            login_device=meta_data.login_device,
            login_method=meta_data.login_method,
            logged_in=True,
            authentication_token=encrypt_data(token.encode("utf-8")),
        )
        LoginHistorySerialiser().update_login_history(
            login_history["id"],
            login_data
        )
        return ServiceResponse(
            message="User Authenticated.",
            status=ServiceStatus.SUCCESS,
            data={
                "id": user["id"],
                "token": token,
            },
        )

    def logout_user(self, login_id: UUID):
        """Logs User Out."""

        login_data = UpdateLoginHistory(
            logged_in=False,
            logout_date=datetime.now()
        )
        LoginHistorySerialiser().update_login_history(
            login_id, login_data
        )
        return ServiceResponse(
            message="User No Longer Authenticated.",
            status=ServiceStatus.SUCCESS,
            data={"id": login_id},
        )