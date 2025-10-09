"""Responses: Contains Custom Data Classes for Responses."""

from typing import Optional
from pydantic import BaseModel
from lib.decorators.utils import validate_function_signature
from lib.utils.constants.responses import ServiceStatus


class ServiceResponse(BaseModel):
    """Manages Custom Service Responses."""

    message: str
    status: ServiceStatus
    data: dict | None = None
