"""Authentication: User Authentication Services."""

from datetime import datetime, timedelta
from json import dumps, loads
from uuid import uuid4
from config import AppConfig
from lib.responses import ServiceResponse
from lib.types.user import Logindata, UserData
from lib.utils.constants.responses import ServiceStatus
from lib.utils.constants.users import DateFormat
from lib.utils.encryption.cryptography import decrypt_data, encrypt_data
from lib.utils.encryption.encoders import get_hash_value
from serialisers.user.users import UserSerialiser
from serialisers.warehouse.logins import LoginHistorySerialiser
from services.abstract import AbstractService


class AuthenticationService(AbstractService):
    """Manages Authentication Operations."""

    __instance = None
    ACTIVE = True

    def __new__(cls, *args, **kwargs) -> "AuthenticationService":
        """Singleton Class Constructor."""

        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def register_user(self, email: str, password: str) -> ServiceResponse:
        """Registers User."""

        response = UserSerialiser().create_user(email, password)
        user_id = self.get_public_id(response)
        data = UserSerialiser().get_user(user_id)
        return ServiceResponse(
            message=response, status=ServiceStatus.SUCCESS, data={"user": data}
        )

    def login_user(
        self, email: str, password: str, user_data: Logindata
    ) -> ServiceResponse:
        """Logs a User In."""

        user_id = get_hash_value(email + password, str(AppConfig().salt_value))
        encrypted_user = UserSerialiser().get_user(user_id)
        user = loads(decrypt_data(encrypted_user))

        if isinstance(user.get("login_history", ""), list):
            for login in user["login_history"]:
                self.logout_user(loads(decrypt_data(login))["id"])

        response = LoginHistorySerialiser().create_login_history(user["id"])
        login_id = self.get_public_id(response)
        login_history = LoginHistorySerialiser().get_login_history(login_id)

        session_id = uuid4()
        token = AuthenticationService().__generate_authentication_token__(
            user_id=user["user_id"],
            login_id=login_history["login_id"],
            session_id=str(session_id),
        )
        LoginHistorySerialiser().update_login_history(
            login_history["id"],
            session_id=session_id,
            authentication_token=token,
            **user_data.login.to_dict()
        )
        return ServiceResponse(
            message="User Authenticated.",
            status=ServiceStatus.SUCCESS,
            data={
                "id": user["user_id"],
                "token": token,
            },
        )

    def logout_user(self, login_id: str):
        """Logs User Out."""

        LoginHistorySerialiser().update_login_history(
            login_id, logged_in=False, logout_date=datetime.now()
        )
        return ServiceResponse(
            message="User No Longer Authenticated.",
            status=ServiceStatus.SUCCESS,
            data={"id": login_id},
        )

    @staticmethod
    def __generate_authentication_token__(**kwargs) -> str:
        """Generates a valid JSON Web Token."""

        result = {
            "expires": (datetime.now() + timedelta(days=30)).strftime(
                DateFormat.HYPHEN.value
            ),
        }
        for key, kwarg in kwargs.items():
            result[key] = kwarg

        return encrypt_data(dumps(result).encode())
