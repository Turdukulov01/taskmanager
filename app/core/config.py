from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./tasks.db"  # по умолчанию локальный SQLite

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")


settings = Settings()
