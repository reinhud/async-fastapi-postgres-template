"""Bundling of endpoint routers."""
from fastapi import APIRouter

from app.api.routes import user


router = APIRouter()

router.include_router(user.router, prefix="/user", tags=["User Endpoints"])


