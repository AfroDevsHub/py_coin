"""Data-Classes: Custom Data-Type Checks."""

from typing import Optional
from lib.interfaces.typed_dicts import ContractDict, TransactionDict
from lib.decorators.utils import validate_function_signature
from lib.interfaces.abstract import AbstractType
from lib.interfaces.typed_dicts import UserDict, AccountDict, ProfileDict, SettingsDict


class AccountData(AbstractType):
    """Type Check for Account Related Data."""

    @validate_function_signature(True)
    def __init__(self, data: AccountDict) -> None:
        super().__init__(data)

    def __str__(self) -> str:
        """String Representation of the Object."""

        return f"Type: {str(self.__class__.__name__)}"

    def __repr__(self) -> str:
        """String Representation of the Object."""

        return f"Application Model: {self.__class__.__name__}"


class ProfileData(AbstractType):
    """Type Check for Profile Related Data."""

    @validate_function_signature(True)
    def __init__(self, data: ProfileDict) -> None:
        super().__init__(data)

    def __str__(self) -> str:
        """String Representation of the Object."""

        return f"Type: {str(self.__class__.__name__)}"

    def __repr__(self) -> str:
        """String Representation of the Object."""

        return f"Application Model: {self.__class__.__name__}"


class SettingsData(AbstractType):
    """Type Check for Settings Related Data."""

    @validate_function_signature(True)
    def __init__(self, data: SettingsDict) -> None:
        super().__init__(data)

    def __str__(self) -> str:
        """String Representation of the Object."""

        return f"Type: {str(self.__class__.__name__)}"

    def __repr__(self) -> str:
        """String Representation of the Object."""

        return f"Application Model: {self.__class__.__name__}"


class LoginData(AbstractType):
    """Type Check for Login Meta Data."""

    @validate_function_signature(True)
    def __init__(self, data: UserDict):
        super().__init__(data)

    def __str__(self) -> str:
        """String Representation of the Object."""

        return f"Type: {str(self.__class__.__name__)}"

    def __repr__(self) -> str:
        """String Representation of the Object."""

        return f"Application Model: {self.__class__.__name__}"



class UserData(AbstractType):
    """Type Check for User Data."""

    @validate_function_signature(True)
    def __init__(
        self,
        account: Optional[AccountDict] = None,
        profile: Optional[ProfileDict] = None,
        settings: Optional[SettingsDict] = None,
        login: Optional[UserDict] = None,
    ) -> None:
        """UserData Constructor."""

        if account:
            self.account = AccountData(account)
        if profile:
            self.profile = ProfileData(profile)
        if settings:
            self.settings = SettingsData(settings)
        if login:
            self.login = LoginData(login)
        super().__init__(None)

    def __str__(self) -> str:
        """String Representation of the Object."""

        return f"Type: {str(self.__class__.__name__)}"

    def __repr__(self) -> str:
        """String Representation of the Object."""

        return f"Application Model: {self.__class__.__name__}"


class TransactionData(AbstractType):
    """Type Check for Transaction Data."""

    @validate_function_signature(True)
    def __init__(
        self, receiver_signiture: str, sender_signiture: str, data: TransactionDict
    ):
        """TransactionData Constructor."""

        self.receiver_signiture = receiver_signiture
        self.sender_signiture = sender_signiture
        super().__init__(data)

    def __str__(self) -> str:
        """String Representation of the Object."""

        return f"Type: {str(self.__class__.__name__)}"

    def __repr__(self) -> str:
        """String Representation of the Object."""

        return f"Application Model: {self.__class__.__name__}"


class ContractData(AbstractType):
    """Type Check for Contract Data."""

    @validate_function_signature(True)
    def __init__(
        self, contractor_signiture: str, contractee_signiture: str, data: ContractDict
    ):
        """ContractData Constructor."""

        self.contractor_signiture = contractor_signiture
        self.contractee_signiture = contractee_signiture
        super().__init__(data)

    def __str__(self) -> str:
        """String Representation of the Object."""

        return f"Type: {str(self.__class__.__name__)}"

    def __repr__(self) -> str:
        """String Representation of the Object."""

        return f"Application Model: {self.__class__.__name__}"
