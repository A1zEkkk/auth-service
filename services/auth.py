from fastapi import Depends

from services.user import UserService, get_user_service

from schemas.auth import AuthRequestsUsingPhone, AuthRequestsUsingEmail
from schemas.dto.user import UserDTO

from core.utils import verify_hash_password
from core.exc.validation import InvalidPasswordError


class AuthService:
    def __init__(self, service: UserService):
        self.service = service

    async def auth_user_with_phone(self, data: AuthRequestsUsingPhone)-> UserDTO:
        user = await self.service.get_user_by_phone(data.phone)
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
        user = await self.service.get_user_by_email(data.email)
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

def get_auth_service(service: UserService = Depends(get_user_service))-> AuthService:
    return AuthService(service)