from fastapi import APIRouter, Depends

from src.modules.cryptos.schemas import (
    TransactionRead,
    TransactionAdd,
    CryptoPortfolio,
    TokenSchema,
)
from src.modules.cryptos.services import crypto_service, token_service
from src.users.dependencies import get_current_active_user, get_current_superuser
from src.base.base_model import User
from src.modules.cryptos.crypto.pricer import set_actual_crypto_price, set_actual_crypto_price_no_redis
from src.modules.cryptos.crypto.crypto_storage import redis_manager


router = APIRouter(
    prefix="/cryptos",
    tags=["cryptos"],
)


@router.get("/", response_model=CryptoPortfolio)
async def crypto_portfolio(user: User = Depends(get_current_active_user)):
    portfolio_assets = await crypto_service.get_user_portfolio(user)
    portfolio = CryptoPortfolio(total=123, assets=portfolio_assets)

    # await set_actual_crypto_price()
    # await set_actual_crypto_price_no_redis()
    # print(await redis_manager.get_current_price('BTC'))
    return portfolio


@router.get("/transactions", response_model=list[TransactionRead])
async def crypto_transactions(user: User = Depends(get_current_active_user)):
    transactions = await crypto_service.get_user_transactions(user)
    return transactions


@router.post("/transactions", response_model=TransactionAdd)
async def add_crypto_transactions(
    transaction: TransactionAdd,
    user: User = Depends(get_current_active_user),
):
    new_transaction = await crypto_service.add_transaction(transaction, user)
    return new_transaction


@router.patch("/transactions/{pk}", response_model=TransactionAdd)
async def update_crypto_transactions(
    pk: int,
    transaction: TransactionAdd,
    user: User = Depends(get_current_active_user),
):
    # how protect not users transaction
    new_transaction = await crypto_service.update_transaction(transaction, user, pk)
    return new_transaction


@router.get("/token/update", status_code=200)
async def update_token_list(user: User = Depends(get_current_superuser)):
    await token_service.update_token_list()


@router.get("/token/search", status_code=200, response_model=list[TokenSchema])
async def search_token(
    token_symbol: str, user: User = Depends(get_current_active_user)
):
    return await token_service.search_token(token_symbol)
