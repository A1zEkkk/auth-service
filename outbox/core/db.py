from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


async_engine = create_async_engine(
    "sqlite+aiosqlite:///outbox.db"
)

session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
