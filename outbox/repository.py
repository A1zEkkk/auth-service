from aiormq.tools import awaitable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import select, delete
from .models import OutBox
from .core.db import session_factory

class OutBoxRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, queue_name, message):
        print("CREATE CALLED")

        stmt = insert(OutBox).values(
            queue_name=queue_name,
            message=message,
        )

        result = await self.db.execute(stmt)
        print(result)

        await self.db.commit()
        print("COMMIT")

        return result

    async def get_first(self):
        stmt = select(OutBox).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self):
        stmt = select(OutBox)
        result = await self.db.execute(stmt)
        return result.all()

    async def delete(self, data_id):
        stmt = delete(OutBox).where(OutBox.id == data_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result

    async def delete_all(self):
        stmt = delete(OutBox)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result



def get_outbox_repository() -> OutBoxRepository:
    session = session_factory()
    return OutBoxRepository(session)


