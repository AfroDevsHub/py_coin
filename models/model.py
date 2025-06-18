"""Model: Base Model for Creating Models."""

from datetime import date, datetime

from uuid import UUID

from lib.utils.constants.users import DateFormat, DateTimeFormat


class BaseModel:
    """A Base/Abstract Model."""

    __table__ = None
    __EXCLUDE_ATTRIBUTES__: list[str] = []

    def __str__(self) -> str:
        """String Representation of the Base Class."""

        return "Abstract/Base Model."

    def __repr__(self) -> str:
        """String Representation of the Base Class."""

        return f"Application Model: {self.__class__.__name__}"

    def to_dict(self):
        """Converts a Model to a Python Dictionary."""
        data = {}
        for key in self.__table__.columns:
            if key.name in self.__EXCLUDE_ATTRIBUTES__:
                continue
            value = getattr(self, key.name)
            if isinstance(value, datetime):
                data[key.name] = value.strftime(DateTimeFormat.HYPHEN.value)
            elif isinstance(value, date):
                data[key.name] = value.strftime(DateFormat.HYPHEN.value)
            elif isinstance(value, UUID):
                data[key.name] = str(value)
            else:
                data[key.name] = value
        return data
