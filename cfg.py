import os

from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV = os.path.join(os.path.dirname(__file__), '.env')


class Settings(BaseSettings):
    algorithm: str
    secret_key: str

    access_m: int

    refresh_m: int
    refresh_h: int
    refresh_d: int

    model_config = SettingsConfigDict(env_file=DOTENV)
