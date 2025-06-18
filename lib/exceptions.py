"""Exceptions: Contains Custom Error Types."""


class ApplicationError(Exception):
    """Custom Error For Application Operations."""

    def __init__(self, message: str) -> None:
        """ApplicationError Constructor."""
        super().__init__(message)
        self.message = message


class FernetError(Exception):
    """Custom Error For Fernet Keys."""

    def __init__(self, message: str) -> None:
        """FernetError Constructor."""

        super().__init__(message)
        self.message = message


class UserError(Exception):
    """Custom Error For Invalid User Operations."""

    def __init__(self, message: str) -> None:
        """UserError Constructor."""

        super().__init__(message)
        self.message = message


class AccountError(Exception):
    """Custom Error For User Account (Users) Models."""

    def __init__(self, message: str) -> None:
        """AccountError Constructor."""

        super().__init__(message)
        self.message = message


class UserProfileError(Exception):
    """Custom Error For User Profile Model."""

    def __init__(self, message: str) -> None:
        """UserProfileError Constructor."""

        super().__init__(message)
        self.message = message


class PaymentProfileError(Exception):
    """Custom Error For Invalid Payment Informations."""

    def __init__(self, message: str) -> None:
        """PaymentProfileError Constructor."""

        super().__init__(message)
        self.message = message


class CardValidationError(Exception):
    """Custom Error For Invalid Card Informations."""

    def __init__(self, message: str) -> None:
        """CardValidationError Constructor."""

        super().__init__(message)
        self.message = message


class SettingsProfileError(Exception):
    """Custom Error For User Settings Errors."""

    def __init__(self, message: str) -> None:
        """SettingsProfileError Constructor."""

        super().__init__(message)
        self.message = message


class LoginHistoryError(Exception):
    """Custom Error For User Login History Errors."""

    def __init__(self, message: str) -> None:
        """LoginHistoryError Constructor."""

        super().__init__(message)
        self.message = message


class TransactionError(Exception):
    """Custom Error For User Transaction Errors."""

    def __init__(self, message: str) -> None:
        """TransactionError Constructor."""

        super().__init__(message)
        self.message = message


class ContractError(Exception):
    """Custom Error For User Contract Errors."""

    def __init__(self, message: str) -> None:
        """ContractError Constructor."""

        super().__init__(message)
        self.message = message


class BlockError(Exception):
    """Custom Error For User Block Errors."""

    def __init__(self, message: str) -> None:
        """BlockError Constructor."""

        super().__init__(message)
        self.message = message


class CLIError(Exception):
    """Custom Error For User CLI Errors."""

    def __init__(self, message: str) -> None:
        """CLIError Constructor."""

        super().__init__(message)
        self.message = message
