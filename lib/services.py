from pydantic import BaseModel

from lib.interfaces.user.accounts import UpdateAccountData
from lib.interfaces.user.payments import UpdatePaymentProfileData
from lib.interfaces.user.profiles import UpdateUserProfileData
from lib.interfaces.user.settings import UpdateSettingsProfileData
from lib.utils.constants.users import Country, LoginMethod


class LoginData(BaseModel):
    login_location: Country | None = None
    login_device: str | None = None
    login_method: LoginMethod | None = None

class UserUpdateData(BaseModel):
    account: UpdateAccountData | None = None
    profile: UpdateUserProfileData | None = None
    settings: UpdateSettingsProfileData | None = None
    payments: UpdatePaymentProfileData | None = None