from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.manager import current_active_user
from src.crypto.crud import add_crypto_transaction, get_user_transactions
from src.config.db.database import db_helper
from src.models.auth import User
from src.schemas.crypto import TransactionRead, TransactionAdd, TransactionUpdate
from src.services.crypto import CryptoService, crypto_service

router = APIRouter(
    prefix='/crypto',
    tags=['crypto'],
)


@router.get("/")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@router.get("/transactions",
            response_model=list[TransactionRead])
async def crypto_transactions(user: User = Depends(current_active_user)):
    transactions = await crypto_service.get_user_transaction(user)
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
