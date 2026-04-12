from .service import UserService
from api.v1.schemas.requests.user import UserCreate

class UserView:
    def __init__(self, user_service: UserService = UserService()):
        self.user_service = user_service

    async def create_user(self, user: UserCreate):
        return await self.user_service.create_user(user)

    async def get_user_by_phone(self, phone: str):
        return await self.user_service.get_user_by_phone(phone)

    async def get_user_by_email(self, email: str):
        return await self.user_service.get_user_by_email(email)