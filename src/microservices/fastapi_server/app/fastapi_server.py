#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""FastAPI server.

Main file of FastAPI application.

TODO:
    * module lvl:
        1. Improve comments and logging
    
    * app lvl:
        1. create test env with own docker-compose and dockerfile and prod.env

@Author: Lukas Reinhardt
@Maintainer: Lukas Reinhardt
"""
import os

from fastapi import FastAPI
from loguru import logger

from app.api.routes.router import router as api_router
from app.core.config import add_middleware, get_app_settings


def get_app() -> FastAPI:
    """Instanciating and setting up FastAPI application"""
    settings = get_app_settings()

    settings.configure_logging()

    app = FastAPI(**settings.fastapi_kwargs)

    add_middleware(app)

    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = get_app()



# ===== App Info Endpoints ===== #
@app.get("/")
async def root():
    return {"message": "OK"}

@app.get("/root_test")
async def get_app_info():
    settings = get_app_settings()
    info = {
        "app_env": settings.app_env,
        "db_settings": settings.database_settings,
        "database url": settings.database_url,
        "app info": settings.fastapi_kwargs,
        "test_env_files": os.getenv("test_var")
    }

    return info

@app.get("/logger_test")
async def test_logger():
    logger.info("This is an info")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.critical("Shit's about to blow up")

    return {"message": "See log types produced"}
