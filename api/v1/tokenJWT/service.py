from core.configs import get_settings, Settings
from api.v1.schemas.requests.token_schema import TokenData
from core.exceptions.domain import TokenError
from authlib.jose import jwt, JWTClaims
from authlib.jose.errors import (
    DecodeError,
    InvalidTokenError,
    BadSignatureError,
    ExpiredTokenError,
    InvalidClaimError,
    MissingClaimError,
)

class TokenService:
    def __init__(self):
        self.settings = get_settings()

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

    async def get_data_from_token(self, token: str) -> JWTClaims:
        try:
            # Сначала декодируем токен
            claims = jwt.decode(token, key=self.settings.JWT_SECRET_KEY)

            # Затем проверяем claims (рекомендуется всегда делать)
            claims.validate()

            return claims

        except BadSignatureError:
            raise TokenError("Invalid token signature")
        except ExpiredTokenError:
            raise TokenError("Token has expired")
        except InvalidClaimError as e:
            raise TokenError(f"Invalid claim: {str(e)}")
        except MissingClaimError as e:
            raise TokenError(f"Missing required claim: {str(e)}")
        except DecodeError:
            raise TokenError("Failed to decode token")
        except InvalidTokenError:
            raise TokenError("Invalid token")

    async def is_refresh_token(self, token: str):
        claims = await self.get_data_from_token(token)
        if claims.header['typ']!='refresh_token':
            raise TokenError("Invalid token type")


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


        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return data



def get_token_service() -> TokenService:
    return TokenService()