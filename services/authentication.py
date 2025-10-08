"""Authentication: User Authentication Services."""

<<<<<<< HEAD
from datetime import datetime, timedelta
from json import dumps, loads
from uuid import uuid4
from config import AppConfig
from lib.responses import ServiceResponse
from lib.types.user import Logindata, UserData
=======
from datetime import datetime
from typing import Any, cast
from uuid import UUID, uuid4

from pydantic import validate_call

from lib.decorators.services import handle_service_errors
from lib.interfaces.responses import ServiceResponse
from lib.interfaces.services import LoginData
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
from lib.utils.constants.responses import ServiceStatus
from lib.utils.helpers.users import generate_jwt_token
from serialisers.user.users import CreateUserData, UserSerialiser
from serialisers.warehouse.logins import (
    CreateLoginHistory,
    LoginHistorySerialiser,
    UpdateLoginHistory,
)


class AuthenticationService:
    """Manages Authentication Operations."""

    __instance = None
    ACTIVE = True

    def __new__(cls, *args: Any, **kwargs: Any) -> "AuthenticationService":
        """Singleton Class Constructor."""

        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

<<<<<<< HEAD
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
=======
    @handle_service_errors
    @validate_call
    def register_user(self, email: str, password: str) -> ServiceResponse:
        """Registers User."""

        user_data = CreateUserData(email=email, password=password)
        user = UserSerialiser().create(user_data)
        print(f"User Registered: {user.id} | Email: {user.email}")
        return ServiceResponse(
            message="User Registered Successfully.",
            status=ServiceStatus.SUCCESS,
            data={"user": user},
        )

    @handle_service_errors
    @validate_call
    def login_user(
        self, email: str, password: str, meta_data: LoginData
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
    ) -> ServiceResponse:
        """Logs a User In."""

        user_id = UserSerialiser().get_user_id(
            CreateUserData(email=email, password=password)
        )
        user = UserSerialiser().read(user_id)

        for login in user.login_history:
            if login.logged_in:
                self.logout_user(login.id)

        login = LoginHistorySerialiser().create(
            CreateLoginHistory(user_id=cast(UUID, user.id))
        )

        session_id = uuid4()
        token = generate_jwt_token(
            user_id=str(user.id),
            login_id=str(login.id),
            session_id=str(session_id),
            email=str(user.email),
        )
        login_data = UpdateLoginHistory(
            session_id=session_id,
            login_location=meta_data.login_location,
            login_device=meta_data.login_device,
            login_method=meta_data.login_method,
            logged_in=True,
            authentication_token=token,
        )
        login = LoginHistorySerialiser().update(cast(UUID, login.id), login_data)
        print(f"User Logged In: {user.id} | Email: {user.email} | Token: {token}")

        return ServiceResponse(
            message="User Authenticated.",
            status=ServiceStatus.SUCCESS,
            data={
                "user": user,
                "login": login,
            },
        )

    @handle_service_errors
    @validate_call
    def logout_user(self, login_id: UUID) -> ServiceResponse:
        """Logs User Out."""

        login_data = UpdateLoginHistory(logged_in=False, logout_date=datetime.now())
        login = LoginHistorySerialiser().update(login_id, login_data)
        print(f"User Logged Out: {login_id}")
        return ServiceResponse(
            message="User No Longer Authenticated.",
            status=ServiceStatus.SUCCESS,
<<<<<<< HEAD
            data={"id": login_id},
=======
            data={
                "login": login,
            },
>>>>>>> ce27e146fbe2699dc419332232c255e5239efcf9
        )
