from fastapi import APIRouter
from views.api.user import router as health_router

router = APIRouter()

router.include_router(health_router, prefix="/user", tags=["user"])
