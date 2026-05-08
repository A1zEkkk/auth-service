from log.app import LoggingMiddleware
from .db.db import AsyncDatabaseSession, database
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.v1.router import router
from .exceptions.base import MainException
from .exceptions.utils import app_exception_handler



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения FastAPI.
    Выполняет инициализацию базы данных при старте приложения и
    корректное отключение при завершении работы.
    """
    await database.init()
    await database.create_all()
    try:
        yield
    finally:
        await database.disconnect()


def create_app():
    app = FastAPI(
        title="Сервис Авторизации",
        lifespan=lifespan
    )

    app.add_middleware(LoggingMiddleware)
    app.include_router(router)
    app.add_exception_handler(MainException, app_exception_handler)


    return app



