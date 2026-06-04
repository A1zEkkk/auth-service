from fastapi import APIRouter

from api.v1.routes.auth import auth_router
from api.v1.routes.register import register_router
from api.v1.routes.refresh import refresh_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(register_router)
router.include_router(refresh_router)
