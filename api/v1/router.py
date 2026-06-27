from fastapi import APIRouter

from api.v1.routes.auth import router as auth_router
from api.v1.routes.register import router as register_router
from api.v1.routes.refresh import router as refresh_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(register_router)
router.include_router(refresh_router)
