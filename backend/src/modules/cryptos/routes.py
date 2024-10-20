from fastapi import APIRouter, Depends

from backend.src.modules.cryptos.schemas import CryptoPortfolioSchema, TransactionRead, TransactionAdd
from backend.src.modules.cryptos.services import crypto_service, token_service
from backend.src.base.base_model import User
from backend.src.modules.common.schemas import BaseAsset
from backend.src.users.dependencies import get_current_active_user, get_current_superuser
from backend.src.modules.cryptos.crypto.graph import TimePeriod


router = APIRouter(
    prefix="/cryptos",
    tags=["cryptos"],
)


@router.get("/", response_model=CryptoPortfolioSchema)
async def crypto_portfolio(user: User = Depends(get_current_active_user)):
    portfolio = await crypto_service.get_user_portfolio(user)
    return portfolio


@router.get("/transactions", response_model=list[TransactionRead])
async def crypto_transactions(user: User = Depends(get_current_active_user)):
    transactions = await crypto_service.get_user_transactions(user)
    return transactions


@router.post("/transactions", response_model=TransactionRead)
async def add_crypto_transactions(
    transaction: TransactionAdd,
    user: User = Depends(get_current_active_user),
):
    """
    Передавать без user_id
    """
    new_transaction = await crypto_service.add_transaction(transaction, user)
    return new_transaction


@router.patch("/transactions/{id}", response_model=TransactionRead)
async def update_crypto_transactions(
    id: int,
    transaction: TransactionAdd,
    user: User = Depends(get_current_active_user),
):
    """
    Передавать без user_id
    """

    new_transaction = await crypto_service.update_transaction(transaction, user, id)
    return new_transaction

@router.delete("/transactions/{id}", status_code=200)
async def delete_crypto_transactions(
    id: int,
    user: User = Depends(get_current_active_user),
):
    """
    Передавать без user_id
    """
    await crypto_service.delete_transaction(user, id)
    return {"detail": "Transaction successfully deleted"}


@router.get("/token/update", status_code=200)
async def update_token_list(user: User = Depends(get_current_superuser)):
    await token_service.update_token_list()
    return {"result": "success"}


@router.get("/token/balance", status_code=200)
async def get_users_token_balance(
    token_id: int, user: User = Depends(get_current_active_user)
) -> float:
    balance = await crypto_service.get_token_balance(user, token_id)
    return balance


@router.get("/token/search", status_code=200, response_model=list[BaseAsset])
async def search_token(
        token_symbol: str,
        limit: int = 100,
        offset: int = 0,
        user: User = Depends(get_current_active_user)
):
    return await token_service.search_token(token_symbol, limit, offset)


@router.get("/graph", status_code=200)
async def get_graph(
    time_period: TimePeriod, user: User = Depends(get_current_active_user)
):
    graph = await crypto_service.get_graph(time_period, user)
    return {"graph_data": graph}
