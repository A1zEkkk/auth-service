from fastapi import APIRouter, Depends
from api.v1.schemas.requests.refresh import RefreshToken
from .refresh import get_refresh_token_use_case, RefreshTokenUseCase

refresh_router = APIRouter()


@refresh_router.post("/refresh")
async def refresh(request: RefreshToken, refresh_token_use_case: RefreshTokenUseCase = Depends(get_refresh_token_use_case)):
    return await refresh_token_use_case.refresh_tokens(refresh_token=request.refresh_token)
