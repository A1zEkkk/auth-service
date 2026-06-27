from fastapi import APIRouter, Depends
from schemas.refresh import RefreshToken
from use_cases.refresh import get_refresh_token_use_case, RefreshTokenUseCase

router = APIRouter()


@router.post("/refresh")
async def refresh(request: RefreshToken, refresh_token_use_case: RefreshTokenUseCase = Depends(get_refresh_token_use_case)):
    return await refresh_token_use_case.refresh_tokens(refresh_token=request.refresh_token)
