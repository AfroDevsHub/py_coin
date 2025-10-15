"""Authentication: User Authentication Services."""

from datetime import datetime
from typing import Any, cast
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import validate_call

from src.lib.decorators.services import handle_service_errors
from src.lib.interfaces.responses import ServiceResponse
from src.lib.types.services.user import LoginUserMetaData
from src.lib.types.user.users import CreateUserData
from src.lib.types.warehouse.login_history import CreateLoginHistory, UpdateLoginHistory
from src.lib.utils.constants.responses import ServiceStatus
from src.lib.utils.constants.users import Status
from src.lib.utils.helpers.users import (
    JWTSignature,
    decode_jwt_token,
    generate_jwt_token,
)
from src.serialisers.user.users import UserSerialiser
from src.serialisers.warehouse.logins import LoginHistorySerialiser

oauth2_scheme = HTTPBearer()


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
        self, email: str, password: str, meta_data: LoginUserMetaData
    ) -> ServiceResponse:
        """Logs a User In."""

        user_id = UserSerialiser().get_user_by_email_and_password(
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
            data={
                "login": login,
            },
        )

    async def verify_jwt_token(
        self, token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
    ) -> JWTSignature:
        print("Verifying JWT token")
        decoded_data = decode_jwt_token(token.credentials)

        if not decoded_data:
            raise HTTPException(status_code=401, detail="Invalid JWT token")

        user = UserSerialiser().read(UUID(decoded_data.user_id))

        if not user:
            raise HTTPException(status_code=401, detail="User Does Not Exist")

        print(f"User status: {user.status}")

        if bool(user.status in [Status.DELETED, Status.INACTIVE]):
            raise HTTPException(status_code=403, detail="User Account is Inactive")

        print(f"JWT verified for user {decoded_data.email}")
        return decoded_data

