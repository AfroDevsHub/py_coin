"""Serialiser: Base Serialiser for model Model."""

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from sqlalchemy.orm.decl_api import DeclarativeMeta

class ISerialiser(ABC):
    """A Base/Abstract Serialiser."""

    @abstractmethod
    def create(self, data: Any) -> DeclarativeMeta:
        pass

    @abstractmethod
    def read(self, model_id: UUID) -> DeclarativeMeta:
        pass

    @abstractmethod
    def update(self, model_id: UUID, data: Any) -> DeclarativeMeta:
        pass

    @abstractmethod
    def delete(self, model_id: UUID) -> str:
        pass
