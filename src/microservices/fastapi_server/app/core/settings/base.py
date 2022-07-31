from enum import Enum

from pydantic import BaseSettings


class AppEnvTypes(Enum):
    prod: str = "prod"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    """Select environment based on 'APP_ENV' in .env file.

    Production environment is used by default.
     """
    app_env: AppEnvTypes #= AppEnvTypes.prod

    class Config:
        env_file = "./environments/.env"
        env_file_encoding = "utf-8"
        
        