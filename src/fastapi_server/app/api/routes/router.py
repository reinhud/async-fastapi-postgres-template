"""Bundling of endpoint routers.

Import and add all endpoint routers here.
"""
from fastapi import APIRouter

from app.api.routes import user


router = APIRouter()

router.include_router(user.router, prefix="/user", tags=["User Endpoints"])


