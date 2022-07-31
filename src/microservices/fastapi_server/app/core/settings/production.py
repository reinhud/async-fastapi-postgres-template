from pydantic import PostgresDsn

from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    app_env: str = "prod"

    # database settings
    postgres_driver: str = "asyncpg"
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: int
    postgres_db: str
    class Config(AppSettings.Config): # AppSettings.Config
        env_file = "./environments/prod.env"
        env_file_encoding = "utf-8"



