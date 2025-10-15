"""CustomErrors: Contains Custom Error Types."""

class CustomError(Exception):
    """Base Custom Error."""

    def __init__(self, message: str, status_code: int) -> None:
        """CustomError Constructor."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ApplicationError(CustomError):
    """Custom Error For Application Operations."""

    def __init__(self, message: str) -> None:
        """ApplicationError Constructor."""

        super().__init__(message, status_code=500)
        self.message = message

class FernetError(CustomError):
    """Custom Error For Fernet Keys."""

    def __init__(self, message: str) -> None:
        """FernetError Constructor."""

        super().__init__(message, status_code=500)
        self.message = message


class UserError(CustomError):
    """Custom Error For Invalid User Operations."""

    def __init__(self, message: str) -> None:
        """UserError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class AccountError(CustomError):
    """Custom Error For User Account (Users) Models."""

    def __init__(self, message: str) -> None:
        """AccountError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class UserProfileError(CustomError):
    """Custom Error For User Profile Model."""

    def __init__(self, message: str) -> None:
        """UserProfileError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class PaymentProfileError(CustomError):
    """Custom Error For Invalid Payment Informations."""

    def __init__(self, message: str) -> None:
        """PaymentProfileError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class CardValidationError(CustomError):
    """Custom Error For Invalid Card Informations."""

    def __init__(self, message: str) -> None:
        """CardValidationError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class SettingsProfileError(CustomError):
    """Custom Error For User Settings Errors."""

    def __init__(self, message: str) -> None:
        """SettingsProfileError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class LoginHistoryError(CustomError):
    """Custom Error For User Login History Errors."""

    def __init__(self, message: str) -> None:
        """LoginHistoryError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class TransactionError(CustomError):
    """Custom Error For User Transaction Errors."""

    def __init__(self, message: str) -> None:
        """TransactionError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class ContractError(CustomError):
    """Custom Error For User Contract Errors."""

    def __init__(self, message: str) -> None:
        """ContractError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class BlockError(CustomError):
    """Custom Error For User Block Errors."""

    def __init__(self, message: str) -> None:
        """BlockError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message


class CLIError(CustomError):
    """Custom Error For User CLI Errors."""

    def __init__(self, message: str) -> None:
        """CLIError Constructor."""

        super().__init__(message, status_code=400)
        self.message = message
