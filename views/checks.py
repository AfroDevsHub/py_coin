from datetime import datetime
from fastapi import APIRouter

from controllers.checks.health import DatabaseCheckController
from controllers.checks.version import VersionCheckController
from lib.types.checks import HealthCheckResponse, VersionCheckResponse

checks_router = APIRouter(prefix="/checks")


@checks_router.get("/health")
def health_check() -> HealthCheckResponse:
    check = DatabaseCheckController()
    models = check.get_models()
    return HealthCheckResponse(**{"database": check.test_models(models)})


@checks_router.get("/version")
def version_check() -> VersionCheckResponse:
    check = VersionCheckController()
    return VersionCheckResponse(**check.confirm_version())
