import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    ENCODING: str = "utf-8"

    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str

    EXPIRE_AT_ACCESS: int = 1800
    EXPIRE_AT_REFRESH: int = 2629743

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str   # имя сервиса в docker-compose
    POSTGRES_PORT: int = 5432
    DB_NAME: str

    DRIVER: str = "postgresql+asyncpg"


    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_VHOST: str = "/"

    @property
    def get_db_url(self):
        return (
            f"{self.DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.DB_NAME}"
        )

    @property
    def get_broker_url(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"
        )

settings = Settings()


@lru_cache()
def get_settings():
    return Settings()
