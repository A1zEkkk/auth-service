from log.app import LoggingMiddleware
from .db.db import async_engine, database
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.v1.routes import router as v1_router
from .exceptions.base import MainException
from .exceptions.utils import app_exception_handler
from core.rabbit.producer import rabbit_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения FastAPI.
    Выполняет инициализацию базы данных при старте приложения и
    корректное отключение при завершении работы.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("insert into roles (id, name) values (1, 'user') on conflict (id) do NOTHING;"))

    await rabbit_producer.connect()
    await rabbit_producer.channel.declare_queue(
        "new_user",
        durable=True
    )

    try:
        yield
    finally:
        await rabbit_producer.close()
        await async_engine.dispose()


def create_app():
    app = FastAPI(
        title="Сервис Авторизации",
        lifespan=lifespan
    )

    app.add_middleware(LoggingMiddleware)
    app.include_router(v1_router, prefix="/api/v1")
    app.add_exception_handler(MainException, app_exception_handler)


    return app



