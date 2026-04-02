from core.db.db import database
from .schemas.requests import UserCreateSchema
from sqlalchemy import insert, selectgit
from .models import UserModel

class UserRepository:

    def __init__(self, db=database):
        self.db= db

    async def create_user(self, user: UserCreateSchema):
        await self.db.rollback()

        user_dict = user.model_dump()

        query = insert(UserModel).values(**user_dict)
        res = await self.db.execute(query)

        return await self.db.commit()


    async def get_user_by_login(self, login):
        await self.db.rollback()

        query = select(UserModel).where(UserModel.email == login)
        res = await self.db.execute(query)
        res = res.scalar()
        await self.db.commit()

        return res

    async def get_user_by_phone(self, phone):
        await self.db.rollback()

        query = select(UserModel).where(UserModel.phone == phone)
        res = await self.db.execute(query)
        res = res.scalar()
        await self.db.commit()

        return res

