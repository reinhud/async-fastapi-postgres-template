#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""FastAPI server.

Main file of FastAPI application.

TODO:
    * app lvl:
        1. Improve logging
        2. create tag metadata with pydantic

    * module lvl:
        	1. improve validation for dates in pydantic,
            only accepts datetimes without the 'Z' suffix.

@Author: Lukas Reinhardt
@Maintainer: Lukas Reinhardt
"""
from fastapi import FastAPI
from loguru import logger

from app.api.routes.router import router as api_router
from app.core.config import add_middleware, get_app_settings
from app.db.db_session import initialize_database


def get_app() -> FastAPI:
    """Instanciating and setting up FastAPI application."""
    settings = get_app_settings()

    app = FastAPI(**settings.fastapi_kwargs)

    add_middleware(app)

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.on_event("startup")
    async def startup_event() -> None:
        await initialize_database()

    settings.configure_logging()

    return app


app = get_app()



# ===== App Info Endpoints ===== #
@app.get("/")
async def root():

    return {"message": "OK"}

@app.get("/settings")
async def get_app_info():
    settings = get_app_settings()
    info = {
        "app_env": settings.app_env,
        "db_settings": settings.database_settings,
        "database url": settings.database_url,
        "app info": settings.fastapi_kwargs,
    }

    return info

@app.get("/logger_test")
async def test_logger():
    logger.info("This is an info")
    logger.warning("This is a warning")
    logger.error("This is an error")
    logger.critical("Shit's about to blow up")

    return {"message": "See log types produced by app"}
