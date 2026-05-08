from fastapi.params import Depends

from api.v1.auth.service import AuthService, get_auth_service
from api.v1.tokenJWT.service import TokenService, get_token_service
from api.v1.refresh.refresh import RefreshService, get_refresh_service
from api.v1.schemas.requests.auth import AuthRequestsUsingPhone, AuthRequestsUsingEmail
from api.v1.schemas.requests.token_schema import TokenData


class AuthUserCase:
    def __init__(self, auth_service: AuthService, token_service: TokenService, refresh_service: RefreshService):
        self.auth_service = auth_service
        self.token_service = token_service
        self.refresh_service = refresh_service

    async def authorization_with_phone(self, data: AuthRequestsUsingPhone):
        user = await self.auth_service.auth_user_with_phone(data)
        token_data = TokenData(
            role=user.role,
            user_id=user.id
        )

        tokens = await self.token_service.get_tokens(token_data)
        refresh_token = tokens['refresh_token']
        await self.refresh_service.insert_token(refresh_token)
        return tokens


    async def authorization_with_email(self, data: AuthRequestsUsingEmail):
        user = await self.auth_service.auth_user_with_email(data)
        token_data = TokenData(
            role=user.role,
            user_id=user.id
        )

        tokens = await self.token_service.get_tokens(token_data)
        refresh_token = tokens['refresh_token']
        await self.refresh_service.insert_token(refresh_token)
        return tokens




def get_auth_user(
        auth_service: AuthService = Depends(get_auth_service),
        token_service: TokenService = Depends(get_token_service),
        refresh_service: RefreshService = Depends(get_refresh_service)
)->AuthUserCase:
    return AuthUserCase(auth_service, token_service, refresh_service)