from fastapi import APIRouter, Depends
from schemas.user import UserCreate
from use_cases.register import RegisterUseCase, get_register_user


router = APIRouter()


@router.post("/register")
async def register_user(request: UserCreate, register_case: RegisterUseCase = Depends(get_register_user)):
    return await register_case.register_user(request)

