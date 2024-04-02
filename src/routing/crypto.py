from fastapi import APIRouter, Depends

from src.utils.manager import current_active_user
from src.models.auth import User
from src.schemas.crypto import TransactionRead, TransactionAdd, CryptoPortfolio
from src.services.crypto import crypto_service

router = APIRouter(
    prefix='/crypto',
    tags=['crypto'],
)


@router.get("/",
            response_model=CryptoPortfolio)
async def crypto_portfolio(user: User = Depends(current_active_user)):
    assets_portfolio = await crypto_service.get_user_portfolio(user)
    portfolio = CryptoPortfolio(total=123,
                                assets=assets_portfolio)
    return portfolio


@router.get("/transactions",
            response_model=list[TransactionRead])
async def crypto_transactions(user: User = Depends(current_active_user)):
    transactions = await crypto_service.get_user_transactions(user)
    return transactions


@router.post("/transactions",
             response_model=TransactionAdd)
async def add_crypto_transactions(transaction: TransactionAdd,
                                  user: User = Depends(current_active_user),
                                  ):
    new_transaction = await crypto_service.add_transaction(transaction, user)
    return new_transaction


@router.patch("/transactions/{pk}",
              response_model=TransactionAdd)
async def update_crypto_transactions(pk: int,
                                     transaction: TransactionAdd,
                                     user: User = Depends(current_active_user),
                                     ):
    # how protect not users transaction
    new_transaction = await crypto_service.update_transaction(transaction, user, pk)
    return new_transaction
