from fastapi import APIRouter, Depends
from schemas.auth import AuthRequestsUsingEmail, AuthRequestsUsingPhone
from use_cases.auth import AuthUserCase, get_auth_user


router = APIRouter()

@router.post("/authP")
async def auth_user_with_phone(request: AuthRequestsUsingPhone, auth_case: AuthUserCase = Depends(get_auth_user)):
    return await auth_case.authorization_with_phone(request)

@router.post("/authE")
async def auth_user_with_email(request: AuthRequestsUsingEmail, auth_case: AuthUserCase = Depends(get_auth_user)):
    return await auth_case.authorization_with_email(request)