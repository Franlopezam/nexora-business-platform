from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nexora"
    debug: bool = True
    secret_key: str = "development-secret-change-me"
    database_url: str = "sqlite:///./nexora.db"
    access_token_minutes: int = 60
    refresh_token_days: int = 7
    rate_limit: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
