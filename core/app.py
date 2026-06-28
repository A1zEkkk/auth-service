import time
from outbox.worker import run_worker
import asyncio
from core.db import Base
from .db.db import async_engine
from fastapi import FastAPI
from sqlalchemy import text
from contextlib import asynccontextmanager
from api.v1.routes import router as v1_router
from .exc.base import DomainError, ValidationError, TokenError, RefreshTokenError

from outbox.core.base import Base as OutboxBase
from outbox.core.db import async_engine as outbox_async_engine

from .exc.utils import domain_exception_handler, token_exception_handler, validation_exception_handler, refresh_token_exception_handler
from core.rabbit.producer import rabbit_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения FastAPI.
    Выполняет инициализацию базы данных при старте приложения и
    корректное отключение при завершении работы.
    """
    async with async_engine.begin() as conn:
        time.sleep(5)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("insert into roles (id, name) values (1, 'user') on conflict (id) do NOTHING;"))

    async with outbox_async_engine.begin() as conn:
        await conn.run_sync(OutboxBase.metadata.create_all)

    await rabbit_producer.connect()
    await rabbit_producer.channel.declare_queue(
        "new_user",
        durable=True
    )

    worker_task = asyncio.create_task(run_worker())

    try:
        yield
    finally:
        worker_task.cancel()

        try:
            await worker_task
        except asyncio.CancelledError:
            pass

        await rabbit_producer.close()
        await async_engine.dispose()
        await outbox_async_engine.dispose()

def create_app():
    app = FastAPI(
        title="Сервис Авторизации",
        lifespan=lifespan
    )

    app.include_router(v1_router, prefix="/api/v1")

    app.add_exception_handler(DomainError, domain_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(TokenError, token_exception_handler)
    app.add_exception_handler(RefreshTokenError, refresh_token_exception_handler)

    return app



