from fastapi import APIRouter

from auth.routes import router as auth_router
from users.routes import router as user_router
from modules.cryptos.routes import router as crypto_router
from modules.stocks.routes import router as stock_router


router = APIRouter(prefix="/api/v1")


def get_apps_router():
    router.include_router(auth_router)
    router.include_router(crypto_router)
    router.include_router(user_router)
    router.include_router(stock_router)
    return router
