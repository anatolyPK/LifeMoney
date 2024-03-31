from fastapi import APIRouter

from .auth import router as auth_router
from .crypto import router as crypto_router


router = APIRouter()


def get_apps_router():
    router.include_router(auth_router)
    router.include_router(crypto_router)
    return router

