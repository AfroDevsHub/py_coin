"""Responses: Contains Custom Data Classes for Responses."""

from datetime import datetime
from typing import Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.lib.utils.constants.responses import ServiceStatus


class ServiceResponse(BaseModel):
    """Manages Custom Service Responses."""

    message: str
    status: ServiceStatus
    data: dict[str, Any] | None = None


class APIResponse(JSONResponse):
    def __init__(
        self,
        data: dict[str, Any],
        message: str = "Request processed successfully",
        status: ServiceStatus = ServiceStatus.SUCCESS,
        status_code: int = 200,
    ) -> None:
        content: dict[str, Any] = {
            "data": data,
            "message": message,
            "status": status.value,
            "timestamp": datetime.now().isoformat(),
        }
        super().__init__(content=content, status_code=status_code)
