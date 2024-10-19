import asyncio


from backend.src.modules.common.schemas import (
    BaseAsset,
    BasePortfolioAsset,
    MainPortfolioInfo,
    BaseTransactionSchema,
    CurrencyEnum,
)
from backend.src.modules.common.redis_storage import redis_manager
from backend.src.modules.common.math import MathOperation
from backend.src.modules.cryptos.schemas import TransactionRead
from backend.src.base.base_model import OperationEnum

class TransactionProcessor:
    def __init__(self, portfolio_maker: "PortfolioMaker", portfolio_asset_scheme):
        self._portfolio_asset_scheme = portfolio_asset_scheme
        self._portfolio_maker = portfolio_maker

    async def process_transactions(self, transactions: list[BaseTransactionSchema]):
        [await self._process_transaction(transaction) for transaction in transactions]

    async def _process_transaction(self, transaction: BaseTransactionSchema):
        asset = self.extract_asset(transaction)
        await self.add_asset_in_portfolio(asset)

        if transaction.operation == OperationEnum.BUY:
            self._summarize_asset(
                asset=asset,
                quantity=transaction.quantity,
                buy_price=transaction.price,
            )
        else:
            self._subtract_asset(
                asset=transaction.asset,
                quantity=transaction.quantity,
            )

    async def add_asset_in_portfolio(self, asset: BaseAsset):
        if asset.id not in self._portfolio_maker._assets:
            current_price = await redis_manager.get_current_price(asset.symbol)
            self._portfolio_maker._assets[asset.id] = self._portfolio_asset_scheme(
                asset=asset,
                current_price=current_price,
            )

    def _summarize_asset(self, asset: BaseAsset, quantity: float, buy_price: float):
        portfolio_asset: BasePortfolioAsset = self._portfolio_maker._assets[asset.id]
        portfolio_asset.average_price_buy = MathOperation.get_new_average_price(
            old_average_price=portfolio_asset.average_price_buy,
            new_price=buy_price,
            old_size=portfolio_asset.quantity,
            new_buy_size=quantity,
        )
        portfolio_asset.quantity += quantity

    def _subtract_asset(self, asset: BaseAsset, quantity: float):
        portfolio_asset: BasePortfolioAsset = self._portfolio_maker._assets[asset.id]
        portfolio_asset.quantity -= quantity

    def extract_asset(self, transaction: BaseTransactionSchema):
        raise NotImplementedError


class PortfolioCalculator:
    def __init__(self, portfolio_maker: "CryptoPortfolioMaker"):
        self.portfolio_maker = portfolio_maker

        self._total_value_rub = 0
        self._total_investment = 0

    async def calculate_assets(self):
        await self._calculate_balances_and_profits()
        await self._calculate_percent_of_portfolio()

    async def _calculate_balances_and_profits(self):
        for asset in self.portfolio_maker._assets.values():
            asset.balance = asset.quantity * asset.current_price
            asset.profit_in_currency, asset.profit_in_percent = (
                MathOperation.get_profits(
                    average_price_buy=asset.average_price_buy * asset.quantity,
                    balance=asset.balance,
                )
            )
            current_price_in_rub, average_price_buy_in_rub = await asyncio.gather(
                self._get_current_price_in_rub(asset),
                self._get_average_price_buy_in_rub(asset)
            )
            self._total_value_rub += asset.quantity * current_price_in_rub
            self._total_investment += asset.quantity * average_price_buy_in_rub

    async def _calculate_percent_of_portfolio(self):
        for asset in self.portfolio_maker._assets.values():
            asset.percent_of_portfolio = MathOperation.get_asset_percent_of_portfolio(
                portfolio_balance=self._total_value_rub,
                assets_balance=asset.quantity * await self._get_current_price_in_rub(asset),
            )

    def calculate_portfolio_info(self) -> MainPortfolioInfo:
        profit_in_currency, profit_in_percent = MathOperation.get_profits(
            average_price_buy=self._total_investment, balance=self._total_value_rub
        )
        return MainPortfolioInfo(
            total_value=self._total_value_rub,
            total_investment=self._total_investment,
            total_profit_in_currency=profit_in_currency,
            total_profit_in_percent=profit_in_percent,
        )

    async def _get_current_price_in_rub(self, asset: BasePortfolioAsset) -> float:
        if asset.currency_type == CurrencyEnum.usd:
            return await self._convert_rub_in_usd(asset.current_price)
        return asset.current_price

    async def _get_average_price_buy_in_rub(self, asset: BasePortfolioAsset) -> float:
        # //TODO вычислять значение usd на необходимую дату
        if asset.currency_type == CurrencyEnum.usd:
            return await self._convert_rub_in_usd(asset.average_price_buy)
        return asset.average_price_buy

    async def _convert_rub_in_usd(self, value: float) -> float:
        return value * await redis_manager.get_usdrub_currency()


class PortfolioMaker:
    def __init__(
        self,
        portfolio_schema,
        portfolio_asset_scheme,
        transaction_processor: type[TransactionProcessor] = TransactionProcessor,
        calculator: type[PortfolioCalculator] = PortfolioCalculator,
    ):
        self._portfolio_schema = portfolio_schema
        self._assets: dict[int, BasePortfolioAsset] = {}
        # Порог для отображения минимальной суммы активов in $
        self._low_balance_threshold = 0.1
        self._transaction_processor = transaction_processor(
            self, portfolio_asset_scheme
        )
        self._calculator = calculator(self)

    async def make_portfolio(self, transactions: list[TransactionRead]):
        await self._transaction_processor.process_transactions(transactions)
        await self._calculator.calculate_assets()

    def _get_portfolio_info(self):
        return self._calculator.calculate_portfolio_info(), self._assets.values()

    @property
    def portfolio(self):
        main_info, assets = self._get_portfolio_info()
        return self._portfolio_schema(main_info=main_info, assets=assets)

    def _hide_assets_with_low_balance(self) -> dict[int, BasePortfolioAsset]:
        return {
            token_id: asset
            for token_id, asset in self._assets.items()
            if asset.balance >= self._low_balance_threshold
        }
