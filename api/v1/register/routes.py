from fastapi import APIRouter, Depends
from api.v1.schemas.requests.user import UserCreate
from .register import RegisterUseCase, get_register_user



register_router = APIRouter()


@register_router.post("/register")
async def register_user(request: UserCreate, register_case: RegisterUseCase = Depends(get_register_user)):
    return await register_case.register_user(request)

