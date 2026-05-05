from fastapi import Depends

from api.v1.user.view import UserView, get_user_view
from api.v1.tokenJWT.service import TokenService, get_token_service
from api.v1.schemas.requests.auth import AuthRequestsUsingPhone, AuthRequestsUsingEmail
from api.v1.schemas.dto.user import UserDTO
from core.utils import verify_hash_password
from core.exceptions.base import InvalidPasswordError, UserNoResultFoundError


class AuthService:
    def __init__(self, user_view: UserView):
        self.user_view = user_view

    async def auth_user_with_phone(self, data: AuthRequestsUsingPhone)-> UserDTO:
        user = await self.user_view.get_user_by_phone(data.phone)
        user_dto = UserDTO.model_validate({
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "phone": user.phone,
            "password": user.password,
            "role": user.role.name
        })
        if not verify_hash_password(data.password, user_dto.password):
            raise InvalidPasswordError

        return user_dto

    async def auth_user_with_email(self, data: AuthRequestsUsingEmail)-> UserDTO:
        user = await self.user_view.get_user_by_email(data.email)
        user_dto = UserDTO.model_validate({
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "phone": user.phone,
            "password": user.password,
            "role": user.role.name
        })
        if not verify_hash_password(data.password, user_dto.password):
            raise InvalidPasswordError

        return user_dto

def get_auth_service(user_view: UserView = Depends(get_user_view))-> AuthService:
    return AuthService(user_view)