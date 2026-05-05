from fastapi import Depends

from core.configs import get_settings, Settings
from api.v1.schemas.requests.token_schema import TokenData
from authlib.jose import jwt, JWTClaims
from api.v1.refresh.service import RefreshService, get_refresh_service


class TokenService:
    def __init__(self, refresh_service: RefreshService, settings: Settings = Depends(get_settings)):
        self.settings = settings
        self.refresh_service = refresh_service

    async def get_token(self, token_data: TokenData):
        header = {
            "alg": self.settings.JWT_ALGORITHM,
            "typ": token_data.type_token,
        }
        payload = {
            "id": token_data.user_id,
            "role": token_data.role,
            "iat": token_data.iat,
            "exp": token_data.exp,
        }

        token = jwt.encode(payload=payload, header=header, key=self.settings.JWT_SECRET_KEY).decode("utf-8")

        return token

    async def verify_token(self, token: str) -> JWTClaims:
        claims = jwt.decode(token, key=self.settings.JWT_SECRET_KEY)
        #Декодирует нашщу шляпу, что бы мо могли получить данные из заголовка и полезной нагрузки
        return claims

    async def get_tokens(self, token_data: TokenData):
        access_data = TokenData(
            type_token="access_token",
            role=token_data.role,
            user_id=token_data.user_id,
        )
        refresh_data = TokenData(
            type_token="refresh_token",
            role=token_data.role,
            user_id=token_data.user_id,
        )

        access_token = await self.get_token(access_data)
        refresh_token = await self.get_token(refresh_data)

        await self.refresh_service.insert_token(refresh_token)

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return data


def get_token_service(refresh_service: RefreshService = Depends(get_refresh_service)) -> TokenService:
    return TokenService(refresh_service)