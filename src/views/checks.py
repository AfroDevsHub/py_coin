from typing import Any
from fastapi import APIRouter

from src.controllers.checks.health import DatabaseCheckController
from src.controllers.checks.version import VersionCheckController
from src.lib.types.checks import HealthCheckResponse, VersionCheckResponse

checks_router = APIRouter(tags=["checks"])


@checks_router.get("/health")
def health_check() -> HealthCheckResponse:
    check = DatabaseCheckController()
    models = check.get_models()
    data: dict[str, Any] = {"database": check.test_models(models)}
    return HealthCheckResponse(**data)

@checks_router.get("/version")
def version_check() -> VersionCheckResponse:
    check = VersionCheckController()
    data: dict[str, Any] = check.confirm_version()
    return VersionCheckResponse(**data)
