from src.base.base_model import OperationEnum
from src.modules.cryptos.schemas import CryptoAsset, TransactionRead, MainPortfolioInfo, CryptoPortfolio, TokenSchema
from src.modules.cryptos.crypto.crypto_storage import redis_manager
from src.modules.cryptos.crypto.math import MathOperation


class TransactionProcessor:
    def __init__(self, portfolio_maker: "CryptoPortfolioMaker"):
        self._portfolio_maker = portfolio_maker

    async def process_transactions(self, transactions: list[TransactionRead]):
        [await self._process_transaction(transaction) for transaction in transactions]

    async def _process_transaction(self, transaction: TransactionRead):
        await self._add_token_in_portfolio(transaction.token)

        if transaction.operation == OperationEnum.BUY: #работает или нет
            self._summarize_token(
                token=transaction.token,
                quantity=transaction.quantity,
                buy_price_in_usd=transaction.price_in_usd
            )
        else:
            self._subtract_token(
                token=transaction.token,
                quantity=transaction.quantity,
            )

    async def _add_token_in_portfolio(self, token: TokenSchema):
        if token.id not in self._portfolio_maker._assets:
            current_price = await redis_manager.get_current_price(token.symbol)
            self._portfolio_maker._assets[token.id] = CryptoAsset(
                token=token,
                current_price=current_price
            )

    def _summarize_token(
            self, token: TokenSchema, quantity: float, buy_price_in_usd: float
    ):
        asset: CryptoAsset = self._portfolio_maker._assets[token.id]
        asset.average_price_buy = MathOperation.get_new_average_price(
            old_average_price=asset.average_price_buy,
            new_price=buy_price_in_usd,
            old_size=asset.quantity,
            new_buy_size=quantity,
        )
        asset.quantity += quantity

    def _subtract_token(
            self, token: TokenSchema, quantity: float
    ):
        asset: CryptoAsset = self._portfolio_maker._assets[token.id]
        asset.quantity -= quantity


class PortfolioCalculator:
    def __init__(self, portfolio_maker: "CryptoPortfolioMaker"):
        self.portfolio_maker = portfolio_maker

        self._total_value = 0
        self._total_investment = 0

    async def calculate_assets(self):
        for asset in self.portfolio_maker._assets.values():
            asset.balance = asset.quantity * asset.current_price
            asset.profit_in_currency, asset.profit_in_percent = (
                MathOperation.get_profits(
                    average_price_buy=asset.average_price_buy * asset.quantity,
                    balance=asset.balance,
                )
            )

            self._total_value += asset.quantity * asset.current_price
            self._total_investment += asset.quantity * asset.average_price_buy

        for asset in self.portfolio_maker._assets.values():
            asset.percent_of_portfolio = MathOperation.get_asset_percent_of_portfolio(
                portfolio_balance=self._total_value,
                assets_balance=asset.balance,
            )

    def calculate_portfolio_info(self) -> MainPortfolioInfo:
        profit_in_currency, profit_in_percent = MathOperation.get_profits(
            average_price_buy=self._total_investment,
            balance=self._total_value
        )
        return MainPortfolioInfo(
            total_value=self._total_value,
            total_investment=self._total_investment,
            total_profit_in_currency=profit_in_currency,
            total_profit_in_percent=profit_in_percent
        )


class CryptoPortfolioMaker:
    def __init__(self):
        self._assets: dict[int, CryptoAsset] = {}
        # Порог для отображения минимальной суммы активов in $
        self._low_balance_threshold = 0.1
        self._transaction_processor = TransactionProcessor(self)
        self._calculator = PortfolioCalculator(self)

    async def make_portfolio(self, transactions: list[TransactionRead]):
        await self._transaction_processor.process_transactions(transactions)
        await self._calculator.calculate_assets()

    @property
    def portfolio(self) -> CryptoPortfolio:
        # assets = self._hide_assets_with_low_balance()
        assets = self._assets
        portfolio_info = self._calculator.calculate_portfolio_info()
        return CryptoPortfolio(
            main_info=portfolio_info,
            assets=assets.values()
        )

    def _hide_assets_with_low_balance(self) -> dict[int, CryptoAsset]:
        return {
            token_id: asset
            for token_id, asset in self._assets.items()
            if asset.balance >= self._low_balance_threshold
        }
