from fastapi import Depends

from .service import UserService, get_user_service
from api.v1.schemas.requests.user import UserCreate

class UserView:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def create_user(self, user: UserCreate):
        return await self.user_service.create_user(user)

    async def get_user_by_phone(self, phone: str):
        return await self.user_service.get_user_by_phone(phone)

    async def get_user_by_email(self, email: str):
        return await self.user_service.get_user_by_email(email)


def get_user_view(user_service: UserService = Depends(get_user_service)):
    return UserView(user_service)