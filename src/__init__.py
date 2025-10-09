"""App: Application Package."""

import logging
import sys
import uvicorn

from fastapi import APIRouter, FastAPI
from src.views.checks import checks_router

# Set up logging configuration
LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format=LOGGER_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"
)

# Get the logger instance
logger = logging.getLogger(__name__)
views_router = APIRouter()
views_router.include_router(checks_router)

app = FastAPI()
app.include_router(views_router)

def handler():
    """Handler function to return the FastAPI app instance."""
    return uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)