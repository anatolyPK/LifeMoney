from fastapi import APIRouter, Depends

from backend.src.modules.stocks.schemas import (
    AssetsSearchResultsSchema,
    ReadTransactionSchema,
    AddTransactionSchema,
    StockPortfolioSchema,
)
from backend.src.modules.stocks.services import stock_service
from backend.src.base.base_model import User
from backend.src.users.dependencies import get_current_active_user

router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
)


@router.get("/", response_model=StockPortfolioSchema, response_model_exclude_none=True)
async def stock_portfolio(user: User = Depends(get_current_active_user)):
    # await set_actual_stock_price()
    # await get_candles_yearly()
    portfolio = await stock_service.get_user_portfolio(user)
    return portfolio


@router.get(
    "/transactions",
    response_model=list[ReadTransactionSchema],
    response_model_exclude_none=True,
)
async def stock_transactions(user: User = Depends(get_current_active_user)):
    transactions = await stock_service.get_user_transactions(user)
    return transactions


@router.post(
    "/transactions",
    response_model=ReadTransactionSchema,
    response_model_exclude_none=True,
)
async def add_stock_transactions(
    transaction: AddTransactionSchema,
    user: User = Depends(get_current_active_user),
):
    """
    Передавать без user_id
    """
    new_transaction = await stock_service.add_transaction(transaction, user)
    return new_transaction


@router.patch(
    "/transactions/{id}",
    response_model=ReadTransactionSchema,
    response_model_exclude_none=True,
)
async def update_stock_transactions(
    id: int,
    transaction: AddTransactionSchema,
    user: User = Depends(get_current_active_user),
):
    """
    Передавать без user_id
    """
    new_transaction = await stock_service.update_transaction(transaction, user, id)
    return new_transaction


@router.get("/asset/balance", status_code=200)
async def get_user_asset_balance(
    figi: str, user: User = Depends(get_current_active_user)
) -> float:
    balance = await stock_service.get_asset_balance(user, figi)
    return balance


@router.get(
    "/assets/search",
    status_code=200,
    response_model=AssetsSearchResultsSchema,
    response_model_exclude_none=True,
)
async def search_assets(
    asset_symbol: str, user: User = Depends(get_current_active_user)
):
    return await stock_service.search_asset(asset_symbol)


# @router.get("/graph", status_code=200)  # , response_model=list[TokenSchema])
# async def get_graph(
#     time_period: TimePeriod, user: User = Depends(get_current_active_user)
# ):
#     graph = await crypto_service.get_graph(time_period, user)
#     return {"ok": graph}


@router.get("/update_assets", status_code=200)
async def update_assets(user: User = Depends(get_current_active_user)):
    await stock_service.update_assets()
    return {"result": "success"}
