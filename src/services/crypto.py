from src.models.auth import User
from src.repositories.base_repository import AbstractRepository
from src.repositories.crypto_repository import crypro_repository
from src.schemas.crypto import TransactionAdd, TransactionAddWithUser, TransactionUpdate, CryptoPortfolio
from src.services.base_service import BaseService
from src.utils.crypto.portfolio import CryptoPortfolioMaker


class CryptoService(BaseService):
    def __init__(self, crypto_repo: AbstractRepository):
        self.crypto_repo: AbstractRepository = crypto_repo

    async def get_user_portfolio(self, user: User):
        transactions = await self.get_user_transactions(user)

        portfolio_maker = CryptoPortfolioMaker()
        return portfolio_maker.make_portfolio(transactions)

    async def add_transaction(self, transaction: TransactionAdd, user: User):
        transaction_with_user_id = TransactionAddWithUser(**transaction.dict(), user_id=user.id)
        added_transaction = await self.crypto_repo.create(transaction_with_user_id)
        return added_transaction

    async def update_transaction(self, transaction: TransactionAdd, user: User, pk: int):
        transaction_with_user_id = TransactionAddWithUser(**transaction.dict(), user_id=user.id)
        added_transaction = await self.crypto_repo.update(transaction_with_user_id, id=pk)
        return added_transaction

    async def get_user_transactions(self, user: User):
        transactions = await self.crypto_repo.get_multi(user_id=user.id)
        return transactions


crypto_service = CryptoService(crypto_repo=crypro_repository)
