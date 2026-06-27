from fastapi import Depends

from schemas.user import UserCreate

from repository.user import UserRepository, get_user_repository

from core.exc.domain.user import ResultNotFoundError, AlreadyExistsError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate):
        data = await self.user_repository.get_user_by_login(user.email)
        if data is not None:
            raise AlreadyExistsError

        data = await self.user_repository.get_user_by_phone(user.phone)
        if data is not None:
            raise AlreadyExistsError

        user_id = await self.user_repository.create_user(user)

        data = await self.user_repository.get_user_by_id(user_id)

        return data

    async def get_user_by_phone(self, phone: str):
        data = await self.user_repository.get_user_by_phone(phone)
        if data is None:
            raise ResultNotFoundError

        return data

    async def get_user_by_email(self, email: str):
        data = await self.user_repository.get_user_by_email(email)
        if data is None:
            raise ResultNotFoundError

        return data


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)