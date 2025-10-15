from typing import Annotated, Any
from uuid import UUID
from fastapi import APIRouter, Depends, Request

from src.lib.interfaces.responses import APIResponse
from src.lib.types.exceptions import CustomError
from src.lib.utils.constants.responses import ServiceStatus
from src.lib.utils.constants.users import Country, LoginMethod
from src.models.user.accounts import Account
from src.models.user.profiles import UserProfile
from src.models.user.settings import SettingsProfile
from src.models.user.users import User
from src.models.warehouse.logins import LoginHistory
from src.serialisers.user.users import UserSerialiser
from src.services.authentication import AuthenticationService
from src.lib.types.services.user import LoginUserMetaData
from src.lib.types.user.users import CreateUserData
from src.services.user import UserService
from src.views.cli.authentication import get_user_meta_data


router = APIRouter(prefix="/user")


@router.get("/")
async def ping() -> APIResponse:
    return APIResponse(
        data={"api": "User", "status": "ACTIVE"},
        message="User API is active",
        status=ServiceStatus.SUCCESS,
        status_code=200,
    )


@router.post("/auth/register")
async def register(user_data: CreateUserData) -> APIResponse:
    try:
        response = AuthenticationService().register_user(
            user_data.email, user_data.password
        )
    except CustomError as exc:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message=str(exc),
            status_code=400,
        )
    if not response.data or "user" not in response.data:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message=response.message,
            status_code=400,
        )

    data: dict[str, Any] = {
        "email": user_data.email,
        "user_id": response.data["user"].user_id,
    }
    return APIResponse(
        data=data,
        message=response.message,
        status=response.status,
        status_code=201,
    )


@router.post("/auth/login")
async def authenticate(user_data: CreateUserData, request: Request) -> APIResponse:
    if request.client:
        info = get_user_meta_data(request.client.host)
    else:
        info = get_user_meta_data()

    login_location = info["country"]
    login_device = info["location"]

    meta_data = LoginUserMetaData(
        login_location=getattr(Country, login_location.upper(), Country.SOUTH_AFRICA),
        login_device=login_device,
        login_method=LoginMethod.EMAIL,
    )
    try:
        response = AuthenticationService().login_user(
            user_data.email, user_data.password, meta_data
        )
    except CustomError as exc:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message=str(exc),
            status_code=401,
        )

    if not response.data or "user" not in response.data or "login" not in response.data:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message=response.message,
            status_code=401,
        )

    user: User = response.data["user"]
    login: LoginHistory = response.data["login"]
    data: dict[str, Any] = {
        "email": user_data.email,
        "token": login.authentication_token,
        "user_id": str(user.user_id),
        "meta_data": {
            "session_id": str(login.session_id),
            "location": login.login_location.value,
            "device": login.login_device,
            "method": login.login_method.value,
        },
    }
    return APIResponse(
        data=data,
        message=response.message,
        status=response.status,
        status_code=200,
    )


@router.get("/accounts/{user_id}")
async def get_user_accounts(
    user_id: UUID,
    token: Annotated[Any, Depends(AuthenticationService().verify_jwt_token)],
) -> APIResponse:
    user = UserSerialiser().read(token.user_id)
    print(f"Setting up account for user: {user_id}, {token.user_id}, {user}")
    if not user or str(user.user_id) != str(user_id):
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message="User Not Authenticated.",
            status_code=403,
        )

    response = UserService().validate_account(token.user_id)

    if not response.data or "account" not in response.data:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message=response.message,
            status_code=404,
        )
    data: dict[str, Any] = {
        "user_id": str(user_id),
        "accounts": [str(account.account_id) for account in response.data["account"]],
    }
    return APIResponse(
        data=data,
        message=response.message,
        status=response.status,
        status_code=200,
    )


@router.post("/account/setup/{user_id}")
async def account_setup(
    user_id: UUID,
    token: Annotated[Any, Depends(AuthenticationService().verify_jwt_token)],
):
    user = UserSerialiser().read(token.user_id)
    print(f"Setting up account for user: {user_id}, {token.user_id}, {user}")
    if not user or str(user.user_id) != str(user_id):
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message="User Not Authenticated.",
            status_code=403,
        )
    response = UserService().validate_account(token.user_id)

    if response.data and len(response.data.get("account", [])) >= 5:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message="User Account not Created - Too Many Existing Accounts",
            status_code=400,
        )

    account = UserService().create_user_account(token.user_id)
    if not account.data:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message="User Account not Created",
            status_code=400,
        )
    data = {
        "account": account.data.get("account", "Account Not Created"),
        "profile": account.data.get("profile", "User Profile Not Created"),
        "settings": account.data.get("settings", "User Settings Profile Not Created"),
    }

    if isinstance(data["account"], Account):
        data["account"] = str(data["account"].account_id)
    
    if isinstance(data["profile"], UserProfile):
        data["profile"] = str(data["profile"].profile_id)
    
    if isinstance(data["settings"], SettingsProfile):
        data["settings"] = str(data["settings"].settings_id)

    return APIResponse(
        data={"account": data},
        status=ServiceStatus.SUCCESS,
        message="User account created successfully",
        status_code=201,
    )
