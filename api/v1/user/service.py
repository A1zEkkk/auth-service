from .repository import UserRepository
from api.v1.schemas.requests.user import UserCreate
from core.exceptions.base import UserAlreadyExistsError, UserNoResultFoundError

class UserService:
    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate):
        data = await self.user_repository.get_by_phone(user.phone)
        if data is not None:
            raise UserAlreadyExistsError

        return await self.user_repository.create(user)

    async def get_user_by_phone(self, phone: str):
        data = await self.user_repository.get_by_phone(phone)
        if data is None:
            raise UserNoResultFoundError

        return data

    async def get_user_by_email(self, email: str):
        data = await self.user_repository.get_by_email(email)
        if data is None:
            raise UserNoResultFoundError

        return data