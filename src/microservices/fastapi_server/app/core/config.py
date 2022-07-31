from functools import lru_cache
from typing import Dict, Type

from fastapi import FastAPI

from app.core.settings.app import AppSettings
from app.core.settings.base import AppEnvTypes, BaseAppSettings
from app.core.settings.production import ProdAppSettings
from app.core.settings.test import TestAppSettings


environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]

    return config()


def add_middleware(app: FastAPI) -> None:
    """Function to implement middleware"""
    pass




