from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.db.db import get_db
from api.v1.schemas.requests.user import UserCreate
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload
from .models import RefreshTokenModel



class RefreshRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_token(self, token: str):
        stmt = insert(RefreshRepository).values(token=token)
        return await self.db.execute(stmt)

    async def get_token(self, token: str):
        stmt = select(RefreshRepository).where(RefreshTokenModel.token == token)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def update_token(self, token: str):
        stmt = update(RefreshRepository).values(is_revoked=True).where(RefreshTokenModel.token == token)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

def get_refresh_repository(db: AsyncSession = Depends(get_db)):
    return RefreshRepository(db)