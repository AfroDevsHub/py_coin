"""Model: Base Model for Creating Models."""

from datetime import date, datetime

from typing import Any
from uuid import UUID

from lib.utils.constants.users import DateFormat, DateTimeFormat
from sqlalchemy import Select

from sqlalchemy.orm import Session
from models import ENGINE
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

    def to_dict(self) -> dict[str, Any]:
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
    
    def test(self) -> bool:
        try:
            with Session(ENGINE) as session:
                data = Select(self.__class__).where(1 == 1)
                session.execute(data)
            return True
        except BaseException as e:
            print(e)
            return False
