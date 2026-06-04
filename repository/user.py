from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.db.db import get_db
from schemas.user import UserCreate
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from models.user import UserModel


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db= db

    async def create_user(self, user: UserCreate):
        user_dict = user.model_dump()
        query = insert(UserModel).values(**user_dict).returning(UserModel.id)
        res = await self.db.execute(query)

        return res.scalar_one()

    async def get_user_by_id(self, user_id: int):
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .where(UserModel.id == user_id)
        )

        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()


    async def get_user_by_login(self, login):
        query = select(UserModel).where(UserModel.email == login)
        res = await self.db.execute(query)
        res = res.scalar_one_or_none()
        return res

    async def get_user_by_phone(self, phone):
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .where(UserModel.phone == phone)
        )
        res = await self.db.execute(stmt)
        res = res.scalar_one_or_none()
        return res

    async def get_user_by_email(self, email):
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .where(UserModel.email == email)
        )
        res = await self.db.execute(stmt)
        res = res.scalar_one_or_none()
        return res

def get_user_repository(db: AsyncSession = Depends(get_db))->UserRepository:
    return UserRepository(db)