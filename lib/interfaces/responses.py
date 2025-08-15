"""Responses: Contains Custom Data Classes for Responses."""

from typing import Any, Optional

from pydantic import BaseModel
from lib.utils.constants.responses import ServiceStatus


class ServiceResponse(BaseModel):
    """Manages Custom Service Responses."""

    message: str
    status: ServiceStatus
    data: dict[str, Any] | None = None
