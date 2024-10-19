from fastapi import APIRouter

from backend.src.auth.routes import router as auth_router
from backend.src.users.routes import router as user_router
from backend.src.modules.cryptos.routes import router as crypto_router
from backend.src.modules.stocks.routes import router as stock_router


router = APIRouter(prefix="/api/v1")


def get_apps_router():
    router.include_router(auth_router)
    router.include_router(crypto_router)
    router.include_router(user_router)
    router.include_router(stock_router)
    return router
