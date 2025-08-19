"""Helpers: Reusable User Functions."""

import jwt
from re import compile as regex_compile
from os import getenv

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


def generate_jwt_token(user_id: str, email: str, login_id: str, session_id: str) -> str:
    """Generates a valid JSON Web Token."""

    result = {
        "iat": datetime.now().strftime(DateFormat.HYPHEN.value),
        "iss": "python-coin",
        "aud": "py-coin",
        "sub": f"py-coin-user-{user_id}",
        "exp": (datetime.now() + timedelta(hours=30)).strftime(DateFormat.HYPHEN.value),
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
