from fastapi import Depends


from .repository import RefreshRepository, get_refresh_repository
from core.utils import hash_token
from datetime import datetime, timezone
from core.exceptions.domain import TokenError


class RefreshService:
    """
    Класс отвечает за добавление токенов в бд, их проверку и отзыв, если оно требуется
    """

    def __init__(self, refresh_repository: RefreshRepository):
        self.refresh_repository = refresh_repository

    async def insert_token(self, token: str):
        hashed_token = hash_token(token)
        result = await self.refresh_repository.create_token(hashed_token)
        return result


    async def verify_token(self, token: str):
        hashed_token = hash_token(token)
        token_obj = await self.refresh_repository.get_token(hashed_token)

        if token_obj is None:
            raise TokenError("Token not found")

        if token_obj.is_revoked:
            raise TokenError("Token revoked")

        if token_obj.exp_at < datetime.now(timezone.utc):
            raise TokenError("Token expired")

        return token_obj

    async def expire_token(self, token: str):
        hashed_token = hash_token(token)
        token_obj = await self.refresh_repository.get_token(hashed_token)
        if token_obj is None:
            raise TokenError("Token not found")

        result = await self.refresh_repository.update_token(hashed_token)
        return result


def get_refresh_service(refresh_repository: RefreshRepository = Depends(get_refresh_repository)):
    return RefreshService(refresh_repository)