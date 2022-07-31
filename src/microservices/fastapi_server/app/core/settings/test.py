from pydantic import PostgresDsn

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    app_env: str  = "test"

    # database settings
    postgres_driver: str = "asyncpg"
    postgres_user: str 
    postgres_password: str 
    postgres_server: str 
    postgres_port: str 
    postgres_db: str 
    class Config(AppSettings.Config):
        env_file = "./environments/test.env"
        env_file_encoding = "utf-8"
