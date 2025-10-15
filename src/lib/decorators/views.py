from typing import Any

from fastapi.responses import JSONResponse

from src.lib.types.exceptions import CustomError


def exception_handler(func: Any) -> Any:
    """Handles View Exceptions."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            print("Decorator Called")
            return func(*args, **kwargs)
        except Exception as exc:
            return JSONResponse(status_code=500, content={"message": str(exc)})

    return wrapper