import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str | None = Field(default=None)
    jwt_secret_key: str = "test-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    mail_username: str = "test@example.com"
    mail_app_password: str = "test-password"
    mail_server: str = "smtp.gmail.com"
    mail_port: int = 587

    def __init__(self, **values):
        if values.get("database_url") is None:
            values["database_url"] = os.getenv("DATABASE_URL") or "sqlite+aiosqlite:///:memory:"
        super().__init__(**values)


settings = Settings()