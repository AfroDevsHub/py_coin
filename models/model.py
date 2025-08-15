"""Model: Base Model for Creating Models."""

from datetime import date, datetime

from typing import Any
from uuid import UUID

from lib.utils.constants.users import DateFormat


class BaseModel:
    """A Base/Abstract Model."""

    def __str__(self) -> str:
        """String Representation of the Base Class."""

        return "Abstract/Base Model."

    def __repr__(self) -> str:
        """String Representation of the Base Class."""

        return f"Application Model: {self.__class__.__name__}"

    def to_dict(self) -> dict[str, Any]:
        """Converts a Model to a Python Dictionary."""

        data: dict[str, Any] = {}
        for key in self.__table__.columns:
            if key.name in self.__EXCLUDE_ATTRIBUTES__:
                continue
            value = getattr(self, key.name)
            if isinstance(value, date):
                data[key.name] = value.strftime(DateFormat.SHORT.value)
            elif isinstance(value, datetime):
                data[key.name] = value.strftime(DateFormat.HYPHEN.value)
            elif isinstance(value, UUID):
                data[key.name] = str(value)
            else:
                data[key.name] = value
        return data
