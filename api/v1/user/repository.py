from core.db.db import database, AsyncDatabaseSession
from api.v1.user.models import UserModel
from api.v1.schemas.requests.user import UserCreate
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from api.v1.schemas.dto.user import UserDTO


class UserRepository:
    def __init__(self, db: AsyncDatabaseSession = database):
        self.db = db

    async def create(self, user: UserCreate):
        stmt = insert(UserModel).values(**user.model_dump()).returning(UserModel.id)
        res = await self.db.execute(stmt)
        user_id = res.scalar_one()
        await self.db.commit()

        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.role))
            .where(UserModel.id == user_id)
        )

        res = await self.db.execute(stmt)
        return res.scalar_one()

    async def get_by_email(self, email: str):
        stmt = (select(UserModel).options(selectinload(UserModel.role)).where(UserModel.email == email))
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_phone(self, phone: str):
        stmt = (select(UserModel).options(selectinload(UserModel.role)).where(UserModel.phone == phone))
        result = await self.db.execute(stmt)
        return result.scalars().first()