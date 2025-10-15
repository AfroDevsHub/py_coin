"""App: Application Package."""

import logging
import sys
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError
import uvicorn

from fastapi import APIRouter, FastAPI, Request
from src.lib.types.exceptions import CustomError
from src.views.checks import checks_router
from src.views.api.user import router as user_router

# Set up logging configuration
LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format=LOGGER_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Get the logger instance
logger = logging.getLogger(__name__)
views_router = APIRouter()
views_router.include_router(checks_router)

app = FastAPI()
app.include_router(views_router)
app.include_router(user_router)


def default_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Default Exception Handler."""
    logger.error(f"Unhandled Exception: {exc}")
    return JSONResponse(content={"message": "Internal Server Error", "status": 500})


@app.exception_handler(CustomError)
async def custom_exception_handler(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=418,
        content={"message": exc.message, "status": "error"},
    )


@app.exception_handler(ExpiredSignatureError)
async def expired_signature_exception_handler(
    request: Request, exc: ExpiredSignatureError
):
    return JSONResponse(
        status_code=401,
        content={"message": "Token has expired", "status": "error"},
    )


app.add_exception_handler(Exception, default_exception_handler)


def handler():
    """Handler function to return the FastAPI app instance."""
    return uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
