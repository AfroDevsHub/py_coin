"""Abstract: Base Service Class."""
from re import compile as regex_compile

from lib.exceptions import UserError


class AbstractService:

    def to_dict(self):
        """Returns a Dictionary representation."""
        return self.__dict__

    @staticmethod
    def get_public_id(value: str) -> str:
        """Retrieve the Public ID from String Representation."""

        regex = regex_compile(r"^.*: (.*)$")
        regex_match = regex.match(value)
        if not regex_match:
            raise UserError("Invalid Public ID String.")
        matches = regex_match.groups()
        if not matches:
            raise UserError("No Valid Public ID.")
        return matches[0]
