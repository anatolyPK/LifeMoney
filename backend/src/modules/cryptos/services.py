from backend.src.base.base_model import Token, OperationEnum, User
from backend.src.core.decorators import timeit

from backend.src.modules.cryptos.crypto.portfolio import CryptoPortfolioMaker
from backend.src.modules.cryptos.crypto.coin_geko_API import CoinGekoAPI
from backend.src.modules.cryptos.crypto.graph import TimePeriod, GraphMaker
from backend.src.modules.cryptos.schemas import TransactionRead, TransactionAdd
from backend.src.base.base_repository import AbstractRepository
from backend.src.base.base_service import BaseService
from backend.src.modules.cryptos.repository import crypro_transactions_repository, token_repository


class CryptoService(BaseService):
    def __init__(self, crypto_repo: AbstractRepository):
        self.crypto_repo: AbstractRepository = crypto_repo

    async def get_user_portfolio(self, user: User):
        transactions: list[TransactionRead] = await self.get_user_transactions(user)
        portfolio_maker = CryptoPortfolioMaker()
        await portfolio_maker.make_portfolio(transactions)
        return portfolio_maker.portfolio

    async def add_transaction(self, transaction: TransactionAdd, user: User):
        transaction_with_user_id = transaction.model_copy(update={"user_id": user.id})
        added_transaction = await self.crypto_repo.create(transaction_with_user_id)
        return added_transaction

    async def update_transaction(
        self, transaction: TransactionAdd, user: User, id_: int
    ):
        transaction_with_user_id = transaction.model_copy(update={"user_id": user.id})
        added_transaction = await self.crypto_repo.update(
            transaction_with_user_id, id=id_
        )
        return added_transaction

    async def get_user_transactions(self, user: User) -> list[TransactionRead]:
        transactions = await self.crypto_repo.get_transactions(user_id=user.id)
        return transactions

    async def get_unique_tokens(self):
        tokens = await self.crypto_repo.get_unique_tokens("token_1")
        return tokens

    async def get_graph(self, time_period: TimePeriod, user: User):
        transactions = await self.get_user_transactions(user)
        graph_maker = GraphMaker(transactions, time_period)
        graph_data = await graph_maker.count_assets_cost()
        return graph_data

    async def get_token_balance(self, user: User, token_id: int):
        transactions = await self.get_user_transactions(user)

        token_balance = sum(
            transaction.quantity
            if transaction.operation == OperationEnum.BUY
            else -transaction.quantity
            for transaction in transactions
            if transaction.token.id == token_id
        )

        return token_balance


class TokenService(BaseService):
    def __init__(self, token_repo: AbstractRepository):
        self.token_repo: AbstractRepository = token_repo

    async def get_single(self, pk: int) -> Token:
        return await self.token_repo.get_single(id=pk)

    @timeit
    async def update_token_list(self):
        updated_tokens = await CoinGekoAPI.get_token_list()
        await self.token_repo.insert_multi(updated_tokens)

    async def search_token(self, token_symbol: str,  limit: int, offset: int):
        return await self.token_repo.search_token(token_symbol.lower(), limit, offset)


# //TODO сделать поиск по символу, потом по cg_id

crypto_service = CryptoService(crypto_repo=crypro_transactions_repository)
token_service = TokenService(token_repo=token_repository)
