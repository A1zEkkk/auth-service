from core.configs import get_settings, Settings
from api.v1.schemas.requests.token_schema import TokenData
from authlib.jose import jwt, JWTClaims


class TokenService:
    def __init__(self, settings: Settings = get_settings()):
        self.settings = settings

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

        token = jwt.encode(payload=payload, header=header, key=self.settings.JWT_SECRET_KEY)

        return token

    def verify_token(self, token: str) -> JWTClaims:
        claims = jwt.decode(token, key=self.settings.JWT_SECRET_KEY)
        #Декодирует нашщу шляпу, что бы мо могли получить данные из заголовка и полезной нагрузки
        return claims

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