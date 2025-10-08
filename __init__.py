"""App: Application Package."""

import logging
import sys

from views.checks import checks_router
from fastapi import APIRouter, FastAPI

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