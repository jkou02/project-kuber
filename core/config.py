"""Configuración centralizada del proyecto."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "postgresql://kubercalc:kubercalc@localhost:5432/kubercalc"
    TELEGRAM_BOT_TOKEN: str = ""
    SECRET_KEY: str = "change-me"
    ENVIRONMENT: str = "development"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


settings = Settings()
