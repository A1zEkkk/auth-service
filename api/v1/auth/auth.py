from api.v1.auth.service import AuthService
from api.v1.tokenJWT.service import TokenService
from api.v1.schemas.requests.auth import AuthRequestsUsingPhone, AuthRequestsUsingEmail
from api.v1.schemas.requests.token import TokenData


class AuthUserCase:
    def __init__(self, auth_service: AuthService = AuthService(), token_service: TokenService = TokenService()):
        self.auth_service = auth_service
        self.token_service = token_service

    async def authorization_with_phone(self, data: AuthRequestsUsingPhone):
        user = await self.auth_service.auth_user_with_phone(data)
        token_data = TokenData(
            role=user.role,
            user_id=user.id
        )

        tokens = self.token_service.get_tokens(token_data)
        return tokens


    async def authorization_with_email(self, data: AuthRequestsUsingEmail):
        user = await self.auth_service.auth_user_with_email(data)
        token_data = TokenData(
            role=user.role,
            user_id=user.id
        )

        tokens = self.token_service.get_tokens(token_data)
        return tokens

def get_auth_user()->AuthUserCase:
    return AuthUserCase()