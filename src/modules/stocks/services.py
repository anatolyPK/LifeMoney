import asyncio
import time
from itertools import chain
from operator import attrgetter

from base.base_model import OperationEnum
from modules.stocks.portfolio import StockPortfolioMaker
from modules.stocks.repository import (
    stock_repository,
    future_repository,
    currency_repository,
    etf_repository,
    bond_repository,
    share_repository,
    future_transaction_repository,
    currency_transaction_repository,
    etf_transaction_repository,
    bond_transaction_repository,
    share_transaction_repository,
)
from modules.stocks.schemas import AssetsSearchResultsSchema, AddTransactionSchema, ReadTransactionSchema
from modules.stocks.tinkoff_api import TinkoffAPI
from src.base.base_repository import AbstractRepository
from src.modules.cryptos.schemas import (
    TransactionAdd,
    TransactionRead,
)
from src.base.base_service import BaseService
from src.core.decorators import timeit
from src.modules.common.portfolio import PortfolioMaker
from src.base.base_model import User
from modules.cryptos.crypto.graph import TimePeriod, GraphMaker


class StockService(BaseService):
    def __init__(self, stock_repo: AbstractRepository):
        self.repository: AbstractRepository = stock_repo

    async def search_asset(self, asset_name: str) -> AssetsSearchResultsSchema:
        tasks = [asset_service.repository.search_asset(asset_name)
                 for asset_service in (share_service, bond_service, etf_service, currency_service, future_service)]
        results = await asyncio.gather(*tasks)
        return AssetsSearchResultsSchema(
            shares=results[0],
            bonds=results[1],
            etfs=results[2],
            currencies=results[3],
            futures=results[4],
        )

    @timeit
    async def update_assets(self):
        asset_fetchers = {
            share_service: TinkoffAPI.get_shares,
            bond_service: TinkoffAPI.get_bonds,
            etf_service: TinkoffAPI.get_etfs,
            currency_service: TinkoffAPI.get_currencies,
            future_service: TinkoffAPI.get_futures,
        }
        fetch_tasks = [
            (asyncio.create_task(fetcher()), asset_service)
            for asset_service, fetcher in asset_fetchers.items()
        ]

        for fetch_task, asset_service in fetch_tasks:
            result = await fetch_task
            await asset_service.repository.create_multi(result["instruments"])


    async def get_user_transactions(self, user: User) -> list[ReadTransactionSchema]:
        transactions = await self.repository.get_user_transaction(user_id=user.id)
        # values = [transaction.values() for transaction in transactions]
        # print('transactionssssssssssssssss')
        # print(values)
        # sorted_values = sorted(values, key=attrgetter('timestamp'), reverse=True)
        return transactions

    async def get_user_portfolio(self, user: User):
        transactions: list[ReadTransactionSchema] = await self.get_user_transactions(user)
        portfolio_maker = StockPortfolioMaker()
        await portfolio_maker.make_portfolio(transactions)
        return portfolio_maker.portfolio

    async def add_transaction(self, transaction: AddTransactionSchema, user: User):
        transaction_with_user_id = transaction.model_copy(update={"user_id": user.id})
        added_transaction = await self.repository.create_transaction(transaction_with_user_id)
        return added_transaction

    async def update_transaction(
            self, transaction: TransactionAdd, user: User, pk: int
    ):
        transaction_with_user_id = transaction.model_copy(update={"user_id": user.id})
        added_transaction = await self.crypto_repo.update(
            transaction_with_user_id, id=pk
        )
        return added_transaction

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

    async def get_assets_price(self) -> dict:
        tasks = [asset_service.repository.get_unique_figis()
                 for asset_service in (share_transaction_service, bond_transaction_service, etf_transaction_service,
                                       currency_transaction_service, future_transaction_service)]
        figis = await asyncio.gather(*tasks)
        flat_figis = list(chain.from_iterable(figis))

        prices_from_api = await TinkoffAPI.get_current_prices(flat_figis)
        return prices_from_api
# class AssetService(BaseService):
#     def __init__(self, repository: AbstractRepository):
#         super().__init__(repository)
#
#         self.asset_fetchers = {
#             'shares': TinkoffAPI.get_shares,
#             'bonds': TinkoffAPI.get_bonds,
#             'etfs': TinkoffAPI.get_etfs,
#             'currencies': TinkoffAPI.get_currencies,
#             'futures': TinkoffAPI.get_futures,
#         }
#
#     async def update_all_assets(self):
#         ...
#
#     async def _update_assets(self, asset_type: str):
#         fetcher = self.asset_fetchers.get(self.asset_type)
#         if fetcher is None:
#             raise ValueError("Unknown asset type")
#
#         assets = await fetcher()
#         await self.repository.create_multi(assets)


share_service = BaseService(repository=share_repository)

bond_service = BaseService(repository=bond_repository)

etf_service = BaseService(repository=etf_repository)

currency_service = BaseService(repository=currency_repository)

future_service = BaseService(repository=future_repository)

stock_service = StockService(stock_repo=stock_repository)



share_transaction_service = BaseService(repository=share_transaction_repository)

bond_transaction_service = BaseService(repository=bond_transaction_repository)

etf_transaction_service = BaseService(repository=etf_transaction_repository)

currency_transaction_service = BaseService(repository=currency_transaction_repository)

future_transaction_service = BaseService(repository=future_transaction_repository)