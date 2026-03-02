from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Engine"
    version: str = "0.1"
    debug: bool = False
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
