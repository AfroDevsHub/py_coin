from typing import Any
from fastapi import APIRouter, Request
import requests

from src.controllers.checks.health import DatabaseCheckController
from src.controllers.checks.version import VersionCheckController
from src.lib.interfaces.responses import APIResponse
from src.lib.types.checks import APIHealthReponse, DatabaseCheckResponse, HealthCheckResponse, VersionCheckResponse
from src.lib.utils.constants.responses import ServiceStatus

checks_router = APIRouter(tags=["checks"])

_API_ENDPOINTS_ = {
    "user": "user"
}

@checks_router.get("/health")
def health_check(request: Request) -> APIResponse:
    check = DatabaseCheckController()
    models = check.get_models()
    data: dict[str, Any] = check.test_models(models)
    databases = DatabaseCheckResponse(**data)
    apis: dict[str, Any] = {}
    for endpoint in _API_ENDPOINTS_:
        api_response = requests.get(f"{request.base_url}{_API_ENDPOINTS_[endpoint]}", timeout=30)
        api_data = APIHealthReponse(**api_response.json()["data"])
        apis[api_data.api] = api_data.status

    response = HealthCheckResponse(database=databases, api=apis)
    return APIResponse(
        data=response.model_dump(),
        message="Health Check Successful",
        status=ServiceStatus.SUCCESS,
        status_code=200,
    )


@checks_router.get("/version")
def version_check() -> APIResponse:
    check = VersionCheckController()
    data: dict[str, Any] = check.confirm_version()
    response = VersionCheckResponse(**data)
    return APIResponse(
        data=response.model_dump(),
        message="Version Check Successful",
        status=ServiceStatus.SUCCESS,
        status_code=200,
    )
