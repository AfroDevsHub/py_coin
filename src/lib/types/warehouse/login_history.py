from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from src.lib.utils.constants.users import Country, LoginMethod


class CreateLoginHistory(BaseModel):
    user_id: UUID


class UpdateLoginHistory(BaseModel):
    session_id: UUID | None = None
    login_location: Country | None = None
    login_device: str | None = None
    login_method: LoginMethod | None = None
    logged_in: bool | None = None
    logout_date: datetime | None = None
    authentication_token: str | None = None
