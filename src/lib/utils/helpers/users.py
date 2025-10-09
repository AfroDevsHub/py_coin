"""Helpers: Reusable User Functions."""

import jwt
from re import compile as regex_compile
from os import getenv

from pydantic import BaseModel

from lib.interfaces.exceptions import UserError

from datetime import datetime, timedelta
from lib.utils.constants.users import DateFormat


def get_public_uuid(value: str) -> str:
    """Retrieve the Public UUID from String Representation."""

    regex = regex_compile(r"^.*: (.*)$")
    regex_match = regex.match(value)
    if not regex_match:
        raise UserError("Invalid Public UUID String.")
    matches = regex_match.groups()
    if not matches:
        raise UserError("No Valid Public UUID.")
    return matches[0]


class JWTSignature(BaseModel):
    iat: int
    iss: str
    aud: str
    sub: str
    exp: int
    email: str
    user_id: str
    login_id: str
    session_id: str


def generate_jwt_token(user_id: str, email: str, login_id: str, session_id: str) -> str:
    """Generates a valid JSON Web Token."""

    result: dict[str, str | int] = {
        "iat": int(datetime.now().timestamp()),
        "iss": "python-coin",
        "aud": "py-coin",
        "sub": f"py-coin-user-{user_id}",
        "exp": int((datetime.now() + timedelta(hours=1)).timestamp()),
        "email": email,
        "user_id": user_id,
        "login_id": login_id,
        "session_id": session_id,
    }
    key = getenv("FERNET_KEY")
    if not key:
        raise ValueError("Fernet Key is not set in environment variables.")

    jwt_token = jwt.encode(result, key, algorithm="HS256")
    return jwt_token


def decode_jwt_token(jwt_token: str) -> JWTSignature:
    key = getenv("FERNET_KEY")
    if not key:
        raise ValueError("Fernet Key is not set in environment variables.")
    
    jwt_data = jwt.decode(jwt_token, key, algorithms=["HS256"], audience="py-coin")
    return JWTSignature(
        **jwt_data
    )
