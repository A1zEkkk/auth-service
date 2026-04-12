from fastapi import APIRouter

from .auth.routes import auth_router
from .register.routes import register_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(register_router)
