from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.ext.asyncio import async_sessionmaker
from core.configs import settings


async_engine = create_async_engine(
            settings.get_db_url,
            future=True,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=10,
            echo_pool='debug',
            pool_recycle=499,
            echo=True,)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db():
    async with async_session() as session:
        async with session.begin():
            yield session