import logging

from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.getLogger('config').setLevel(logging.WARNING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
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

    #   MQTT
    MQTT_CLIENT_ID: str
    MQTT_HOST: str
    MQTT_PORT: int

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgresql+asyncpg".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL for asyncpg.
        """
        url = MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER_MANUFACTORY,
            password=self.POSTGRES_PASSWORD_MANUFACTORY,
            host=self.POSTGRES_HOST_MANUFACTORY,
            path=self.POSTGRES_DB_MANUFACTORY,
        )
        return str(url)

    @computed_field
    @property
    def asyncpg_url_industrial(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgresql+asyncpg".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL for asyncpg.
        """
        url = MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER_INDUSTRIAL,
            password=self.POSTGRES_PASSWORD_INDUSTRIAL,
            host=self.POSTGRES_HOST_INDUSTRIAL,
            path=self.POSTGRES_DB_INDUSTRIAL,
        )
        return str(url)


settings = Settings()
