from fastapi import Depends

from .service import RefreshService, get_refresh_service
from api.v1.tokenJWT.service import TokenService, get_token_service
from api.v1.schemas.requests.token_schema import TokenData


class RefreshTokenUseCase:
    def __init__(self, refresh_service: RefreshService, token_service: TokenService):
        self.refresh_service = refresh_service
        self.token_service = token_service

    async def refresh_tokens(self, refresh_token: str): #returning new token
        await self.token_service.get_data_from_token(refresh_token) # Проверяем подписи и тд
        await self.token_service.is_refresh_token(refresh_token)
        #Проверки на то, что токен существует в бд + отзыв
        await self.refresh_service.verify_token(refresh_token)
        await self.refresh_service.expire_token(refresh_token)

        claims = await self.token_service.get_data_from_token(refresh_token)

        token_data = TokenData(
            user_id=claims["id"],
            role=claims["role"],
        )
        tokens = await self.token_service.get_tokens(token_data)
        refresh_token = tokens["refresh_token"]
        await self.refresh_service.insert_token(refresh_token)

        return tokens


def get_refresh_token_use_case(
        refresh_service: RefreshService = Depends(get_refresh_service),
        token_service: TokenService = Depends(get_token_service)
)->RefreshTokenUseCase:
    return RefreshTokenUseCase(refresh_service, token_service)