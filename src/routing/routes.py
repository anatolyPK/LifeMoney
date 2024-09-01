from fastapi import APIRouter

from src.auth.routes import router as auth_router
from src.users.routes import router as user_router
from src.modules.cryptos.routes import router as crypto_router


router = APIRouter()


def get_apps_router():
    router.include_router(auth_router)
    router.include_router(crypto_router)
    router.include_router(user_router)
    return router

