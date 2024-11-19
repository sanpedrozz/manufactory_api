import logging
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.getLogger('config').setLevel(logging.INFO)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    #   Postgres MANUFACTORY
    POSTGRES_USER_MANUFACTORY: str
    POSTGRES_PASSWORD_MANUFACTORY: str
    POSTGRES_HOST_MANUFACTORY: str
    POSTGRES_DB_MANUFACTORY: str

    #   Postgres INDUSTRIAL
    POSTGRES_USER_INDUSTRIAL: str
    POSTGRES_PASSWORD_INDUSTRIAL: str
    POSTGRES_HOST_INDUSTRIAL: str
    POSTGRES_DB_INDUSTRIAL: str

    #   Telegram-Bot
    BOT_TOKEN_TEST: str
    CHAT_ID_TEST: str
    BOT_TOKEN: str
    CHAT_ID: str

    #   API connect
    API_IP: str
    API_PORT: str
    API_POSTFIX: str

    @staticmethod
    def _get_postgres_url(user: str, password: str, host: str, db: str) -> PostgresDsn:
        url = f"postgresql+asyncpg://{user}:{password}@{host}/{db}"
        return PostgresDsn(url)  # Создание PostgresDsn из строки

    @property
    def manufactory_db_url(self) -> PostgresDsn:
        return self._get_postgres_url(
            self.POSTGRES_USER_MANUFACTORY,
            self.POSTGRES_PASSWORD_MANUFACTORY,
            self.POSTGRES_HOST_MANUFACTORY,
            self.POSTGRES_DB_MANUFACTORY,
        )

    @property
    def industrial_db_url(self) -> PostgresDsn:
        return self._get_postgres_url(
            self.POSTGRES_USER_INDUSTRIAL,
            self.POSTGRES_PASSWORD_INDUSTRIAL,
            self.POSTGRES_HOST_INDUSTRIAL,
            self.POSTGRES_DB_INDUSTRIAL,
        )


settings = Settings()
