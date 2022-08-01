from functools import lru_cache
from typing import Dict, Type

from fastapi import FastAPI

from app.core.app_settings import AppSettings


def get_app_settings() -> AppSettings:
    return AppSettings()


def add_middleware(app: FastAPI) -> None:
    """Function to implement middleware"""
    pass




