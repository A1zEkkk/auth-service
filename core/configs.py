from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import validator

import os


DOTENV = os.path.join(os.path.dirname(__file__), '../.env')

class Settings(BaseSettings):
    JWT_ALGORITHM : str
    JWT_SECRET_KEY : str
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str

    def get_db_url(self):
        return ""

    model_config = SettingsConfigDict(env_file=DOTENV)

settings = Settings()


@lru_cache()
def get_settings():
    return Settings()

print(get_settings())
