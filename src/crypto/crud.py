from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth import CryptoTransaction, User
from src.schemas.crypto import TransactionAdd


# from src.crypto.models import CryptoTransaction


async def add_crypto_transaction(session: AsyncSession,  transaction: TransactionAdd, user: User):
    new_transaction = CryptoTransaction(**transaction.dict(), user=user)
    session.add(new_transaction)
    await session.commit()
    return new_transaction


async def get_user_transactions(session: AsyncSession, user: User):
    statement = select(CryptoTransaction).filter_by(user_id=user.id)
    result = await session.execute(statement)
    transactions = result.scalars().all()
    return transactions
