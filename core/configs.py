import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = os.path.join(os.path.dirname(__file__), '../.env')

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

    def get_db_url(self):
        return (
            f"{self.DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.DB_NAME}"
        )
    model_config = SettingsConfigDict(env_file=DOTENV)

settings = Settings()


@lru_cache()
def get_settings():
    return Settings()
