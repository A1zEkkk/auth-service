from core.configs import get_settings, Settings
from api.v1.schemas.requests.token import TokenData
from authlib.jose import jwt


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

    def verify_token(self, token: bytes):
        return jwt.decode(token, key=self.settings.JWT_SECRET_KEY)

    def get_tokens(self, token_data: TokenData):
        token_data.type_token = "access_token"
        access_token = self.get_token(token_data)
        token_data.type_token = "refresh_token"
        refresh_token = self.get_token(token_data)
        print(access_token)
        print(refresh_token)
        return {"access_token": access_token, "refresh_token": refresh_token}


def get_token_service() -> TokenService:
    return TokenService()