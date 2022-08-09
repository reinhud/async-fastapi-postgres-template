"""App configuration functions and access to settings"""
import os

import alembic
from alembic.config import Config
from fastapi import FastAPI
from loguru import logger
from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
import warnings

from app.core.app_settings import AppSettings
from app.db.models.base import Base


def get_app_settings() -> AppSettings:
    return AppSettings()


def add_middleware(app: FastAPI) -> None:
    """Function to implement middleware.
    
    Not implemented yet.
    """
    pass


