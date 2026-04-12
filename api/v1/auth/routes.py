from fastapi import APIRouter, Depends
from api.v1.schemas.requests.auth import AuthRequestsUsingEmail, AuthRequestsUsingPhone
from .auth import AuthUserCase, get_auth_user


auth_router = APIRouter()

@auth_router.post("/authP")
async def auth_user_with_phone(request: AuthRequestsUsingPhone, auth_case: AuthUserCase = Depends(get_auth_user)):
    return await auth_case.authorization_with_phone(request)

@auth_router.post("/authE")
async def auth_user_with_email(request: AuthRequestsUsingEmail, auth_case: AuthUserCase = Depends(get_auth_user)):
    return await auth_case.authorization_with_email(request)