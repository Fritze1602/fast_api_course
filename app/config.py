from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username:  str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()

# settings = Settings()
