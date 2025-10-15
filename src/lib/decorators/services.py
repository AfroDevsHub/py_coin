from typing import Any, Callable


from src.lib.interfaces.responses import ServiceResponse
from src.lib.utils.constants.responses import ServiceStatus


def handle_service_errors(func: Callable[..., Any]) -> Callable[..., ServiceResponse]:
    """Handles Service Errors."""

    def wrapper(*args: Any, **kwargs: Any) -> ServiceResponse:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            return ServiceResponse(
                message=str(exc),
                status=ServiceStatus.ERROR,
            )

    return wrapper
