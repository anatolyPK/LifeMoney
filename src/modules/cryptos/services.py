from src.base.base_repository import AbstractRepository
from src.modules.cryptos.repository import (
    crypro_transactions_repository,
    token_repository,
)
from src.modules.cryptos.schemas import TransactionAdd, TransactionAddWithUser
from src.base.base_service import BaseService
from modules.cryptos.crypto.portfolio import CryptoPortfolioMaker
from src.base.base_model import User
from modules.cryptos.crypto.coin_geko_API import CoinGekoAPI


class CryptoService(BaseService):
    def __init__(self, crypto_repo: AbstractRepository):
        self.crypto_repo: AbstractRepository = crypto_repo

    async def get_user_portfolio(self, user: User):
        transactions = await self.get_user_transactions(user)
        portfolio_maker = CryptoPortfolioMaker()
        return portfolio_maker.make_portfolio(transactions)

    async def add_transaction(self, transaction: TransactionAdd, user: User):
        transaction_with_user_id = TransactionAddWithUser(
            **transaction.dict(), user_id=user.id
        )
        added_transaction = await self.crypto_repo.create(transaction_with_user_id)
        return added_transaction

    async def update_transaction(
        self, transaction: TransactionAdd, user: User, pk: int
    ):
        transaction_with_user_id = TransactionAddWithUser(
            **transaction.dict(), user_id=user.id
        )
        added_transaction = await self.crypto_repo.update(
            transaction_with_user_id, id=pk
        )
        return added_transaction

    async def get_user_transactions(self, user: User):
        transactions = await self.crypto_repo.get_multi(user_id=user.id)
        return transactions

    async def get_unique_tokens(self):
        tokens = await self.crypto_repo.get_unique_tokens('token_1')
        return tokens


class TokenService(BaseService):
    def __init__(self, token_repo: AbstractRepository):
        self.token_repo: AbstractRepository = token_repo

    async def update_token_list(self):
        updated_tokens = await CoinGekoAPI.get_token_list()
        await self.token_repo.insert_multi(updated_tokens)

    async def search_token(self, token_symbol: str):
        return await self.token_repo.search_token(token_symbol.lower())
# //TODO сделать поиск по символу, потом по cg_id

crypto_service = CryptoService(crypto_repo=crypro_transactions_repository)
token_service = TokenService(token_repo=token_repository)
