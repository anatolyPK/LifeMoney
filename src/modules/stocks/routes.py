from fastapi import APIRouter, Depends

from modules.stocks.schemas import UpdateTimeInfoSchema, AssetsSearchResultsSchema, ReadTransactionSchema, \
    AddTransactionSchema, StockPortfolioSchema
from modules.stocks.services import stock_service
from src.modules.cryptos.schemas import (
    TransactionRead,
    TransactionAdd,
    TokenSchema,
)
from src.modules.cryptos.services import crypto_service, token_service
from src.modules.common.schemas import BasePortfolioSchema
from src.modules.common.redis_storage import redis_manager
from src.users.dependencies import get_current_active_user, get_current_superuser
from src.base.base_model import User
from src.modules.cryptos.crypto.graph import TimePeriod
from src.modules.stocks.pricer import set_actual_stock_price


router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)


@router.get("/", response_model=StockPortfolioSchema, response_model_exclude_none=True)
async def stock_portfolio(user: User = Depends(get_current_active_user)):
    await set_actual_stock_price()
    portfolio = await stock_service.get_user_portfolio(user)
    print(portfolio)
    price = await redis_manager.get_current_price('BBG00475KKY8')
    print('PRICEEEEEEEEEEEEE')
    print(price)
    return portfolio


@router.get("/transactions", response_model=list[ReadTransactionSchema], response_model_exclude_none=True)
async def stock_transactions(user: User = Depends(get_current_active_user)):
    transactions = await stock_service.get_user_transactions(user)
    return transactions


@router.post("/transactions", response_model=ReadTransactionSchema, response_model_exclude_none=True)
async def add_stock_transactions(
    transaction: AddTransactionSchema,
    user: User = Depends(get_current_active_user),
):
    """
    Передавать без user_id
    """
    new_transaction = await stock_service.add_transaction(transaction, user)
    return new_transaction


@router.patch("/transactions/{pk}", response_model=TransactionRead)
async def update_crypto_transactions(
    pk: int,
    transaction: TransactionAdd,
    user: User = Depends(get_current_active_user),
):
    """
    Передавать без user_id
    """

    new_transaction = await crypto_service.update_transaction(transaction, user, pk)
    return new_transaction


@router.get("/token/balance", status_code=200)
async def get_users_token_balance(
    token_id: int, user: User = Depends(get_current_active_user)
) -> float:
    balance = await crypto_service.get_token_balance(user, token_id)
    return balance


@router.get(
    "/assets/search",
    status_code=200,
    response_model=AssetsSearchResultsSchema,
    response_model_exclude_none=True
)
async def search_assets(
        asset_symbol: str,
        user: User = Depends(get_current_active_user)
):
    return await stock_service.search_asset(asset_symbol)


@router.get("/graph", status_code=200)  # , response_model=list[TokenSchema])
async def get_graph(
    time_period: TimePeriod, user: User = Depends(get_current_active_user)
):
    graph = await crypto_service.get_graph(time_period, user)
    return {"ok": graph}


@router.get("/update_assets", status_code=200, response_model=UpdateTimeInfoSchema)
async def update_assets(user: User = Depends(get_current_active_user)):
    operation_time = await stock_service.update_assets()
    return UpdateTimeInfoSchema(operation_time_in_sec=operation_time)
