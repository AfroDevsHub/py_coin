from datetime import datetime
from typing import Annotated, Any
from fastapi import APIRouter, Request
from pydantic import BaseModel

from lib.interfaces.services import LoginData
from lib.interfaces.user.accounts import CreateAccountData
from lib.interfaces.user.users import CreateUserData
from lib.utils.constants.responses import ServiceStatus
from lib.utils.constants.users import Country, LoginMethod
from models.user.users import User
from models.warehouse.logins import LoginHistory
from services.authentication import AuthenticationService
from services.user import UserService
from views.cli.authentication import get_user_meta_data


router = APIRouter()


class APIResponse(BaseModel):
    message: str
    status: ServiceStatus
    data: dict[str, Any]
    timestamp: datetime


@router.post("/auth/register")
async def register(user_data: CreateUserData):
    response = AuthenticationService().register_user(
        user_data.email, user_data.password
    )
    if not response.data or "user" not in response.data:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message=response.message,
            timestamp=datetime.now(),
        )

    data: dict[str, Any] = {
        "email": user_data.email,
        "user_id": response.data["user"].user_id,
    }
    return APIResponse(
        data=data,
        message=response.message,
        status=response.status,
        timestamp=datetime.now(),
    )


@router.post("/auth/login")
async def authenticate(user_data: CreateUserData, request: Request):
    if request.client:
        info = get_user_meta_data(request.client.host)
    else:
        info = get_user_meta_data()

    login_location = info["country"]
    login_device = info["location"]

    meta_data = LoginData(
        login_location=getattr(Country, login_location.upper(), Country.SOUTH_AFRICA),
        login_device=login_device,
        login_method=LoginMethod.EMAIL,
    )
    response = AuthenticationService().login_user(
        user_data.email, user_data.password, meta_data
    )

    if not response.data or "user" not in response.data or "login" not in response.data:
        return APIResponse(
            data={},
            status=ServiceStatus.ERROR,
            message=response.message,
            timestamp=datetime.now(),
        )

    user: User = response.data["user"]
    login: LoginHistory = response.data["login"]
    data: dict[str, Any] = {
        "email": user_data.email,
        "token": login.authentication_token,
        "user_id": user.user_id,
        "meta_data": {
            "session_id": login.session_id,
            "location": login.login_location,
            "device": login.login_device,
            "method": login.login_method,
        },
    }
    return APIResponse(
        data=data,
        message=response.message,
        status=response.status,
        timestamp=datetime.now(),
    )

from fastapi.security import HTTPBearer
from fastapi import APIRouter


oauth2_scheme = HTTPBearer()


async def verify_jwt_token(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> JWTSignature:
    print("Verifying JWT token")
    decoded_data = decode_jwt_token(token.credentials,)


    if not decoded_data:
        raise HTTPException(status_code=401, detail="Invalid JWT token")

    user = UserSerialiser().get_existing_data(
        UserData(email=decoded_data.email, role=decoded_data.role)
    )
    if not user:
        raise HTTPException(status_code=401, detail="User Does Not Exist")

    if not bool(user.active):
        raise HTTPException(status_code=401, detail="User Not Active")

    logger.info(f"JWT verified for user {user.email}")
    return JWTSignature(email=str(user.email), role=str(user.role))

@router.post("/account/setup/{user_id}")
async def account_setup(user_id: UUID, token: Annotated[Any, Depends(verify_jwt_token)]):
    UserService().create_user_account(account_data)
