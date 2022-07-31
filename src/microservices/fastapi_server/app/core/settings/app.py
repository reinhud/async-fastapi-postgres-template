import sys
import logging
from typing import Dict, Any, List, Tuple

from pydantic import PostgresDsn, SecretStr
from loguru import logger

from app.core.settings.base import BaseAppSettings
from app.core.logging import InterceptHandler


class AppSettings(BaseAppSettings):
    # FastAPI App settings
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"

    title: str 
    version: str 
    description: str 
    api_prefix: str = "/api"

    # max_connection_count: int = 10
    # min_connection_count: int = 10
    # secret_key: SecretStr
    # jwt_token_prefix: str = "Token"
    allowed_hosts: List[str] = ["*"]

    # logging
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")


    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
            "description": self.description,
        }
    
    @property
    def database_settings(self) -> Dict[str, Any]:
        return {
            "postgres_user": self.postgres_user,
            "postgres_password": self.postgres_password,
            "postgres_server": self.postgres_server,
            "postgres_port": self.postgres_port,
            "postgres_db": self.postgres_db,
        }
    
    @property
    def database_url(self) -> PostgresDsn:
        return f"postgresql+{self.postgres_driver}://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
    
    
    class Config:
        env_file = "./environments/.env"
        env_file_encoding = "utf-8"


    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
        FORMAT = "[<green>{time}</green>] [<level>{level}</level>] <level>{message}</level>"
        logger.add(sys.stdout, colorize=True, format=FORMAT)