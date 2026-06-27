from core.exc.jwt import *
from core.configs import get_settings

from schemas.JWT import TokenData

from authlib.jose import jwt, JWTClaims
from authlib.jose.errors import *

class TokenService:
    def __init__(self):
        self.settings = get_settings()

    def get_token(self, token_data: TokenData):
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

    def get_data_from_token(self, token: str) -> JWTClaims:
        try:
            # Сначала декодируем токен
            claims = jwt.decode(token, key=self.settings.JWT_SECRET_KEY)

            # Затем проверяем claims
            claims.validate()

            return claims

        except BadSignatureError:
            raise TokenSignatureError
        except ExpiredTokenError:
            raise TokenExpiredError
        except InvalidClaimError:
            raise TokenClaimError
        except MissingClaimError:
            raise TokenClaimError
        except DecodeError:
            raise TokenDecodeError
        except InvalidTokenError:
            raise TokenInvalidError

    def is_refresh_token(self, token: str):
        claims = self.get_data_from_token(token)
        if claims.header['typ']!='refresh_token':
            raise TokenInvalidError


    def get_tokens(self, token_data: TokenData):
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

        access_token = self.get_token(access_data)
        refresh_token = self.get_token(refresh_data)


        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return data



def get_token_service() -> TokenService:
    return TokenService()