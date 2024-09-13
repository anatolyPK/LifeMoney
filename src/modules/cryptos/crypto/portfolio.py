
from base.base_model import OperationEnum
from modules.cryptos.schemas import TokenSchema
from src.modules.cryptos.schemas import CryptoAsset, TransactionRead
from src.modules.cryptos.crypto.crypto_storage import redis_manager
from src.modules.cryptos.crypto.math import MathOperation


class TransactionProcessor:
    def __init__(self, portfolio_maker: "CryptoPortfolioMaker"):
        self._portfolio_maker = portfolio_maker

    def process_transactions(self, transactions: list[TransactionRead]):
        [self._process_transaction(transaction) for transaction in transactions]

    def _process_transaction(self, transaction: TransactionRead):
        token_to_buy, token_to_sell = (
            (transaction.token_1, transaction.token_2)
            if transaction.operation == OperationEnum.BUY
            else (transaction.token_2, transaction.token_1)
        )

        [self._add_token_in_portfolio(token) for token in (token_to_buy, token_to_sell)]

        self._summarize_token(
            token_to_buy, transaction.quantity, transaction.price_in_usd
        )
        self._subtract_token(
            token_to_sell, transaction.quantity, transaction.price_in_usd
        )

    def _add_token_in_portfolio(self, token: TokenSchema):
        if token.id not in self._portfolio_maker._assets:
            self._portfolio_maker._assets[token.id] = CryptoAsset(token=token)

    def _summarize_token(
        self, token: TokenSchema, quantity: float, buy_price_in_usd: float
    ):
        asset = self._portfolio_maker._assets[token.id]
        asset.average_price_buy = MathOperation.get_new_average_price(
            old_average_price=asset.average_price_buy,
            new_price=buy_price_in_usd,
            old_size=asset.quantity,
            new_buy_size=quantity,
        )
        asset.quantity += quantity

    def _subtract_token(
        self, token: TokenSchema, quantity: float, buy_price_in_usd: float
    ):
        asset = self._portfolio_maker._assets[token.id]
        asset.quantity -= quantity
        if asset.quantity < 0:
            asset.quantity = 0


class PortfolioCalculator:
    def __init__(self, portfolio_maker: "CryptoPortfolioMaker"):
        self.portfolio_maker = portfolio_maker

    async def calculate(self):
        for asset in self.portfolio_maker._assets.values():
            asset.current_price = await redis_manager.get_current_price(
                asset.token.symbol
            )
            asset.balance = asset.quantity * asset.current_price
            asset.profit_in_currency, asset.profit_in_percent = (
                MathOperation.get_profits(
                    average_price_buy=asset.average_price_buy * asset.quantity,
                    balance=asset.balance,
                )
            )

        self.portfolio_maker.balance = sum(
            asset.balance for asset in self.portfolio_maker._assets.values()
        )

        for asset in self.portfolio_maker._assets.values():
            asset.percent_of_portfolio = MathOperation.get_asset_percent_of_portfolio(
                portfolio_balance=self.portfolio_maker.balance,
                assets_balance=asset.balance,
            )


class CryptoPortfolioMaker:
    def __init__(self):
        self._assets: dict[int, CryptoAsset] = {}
        self.balance = 0
        self._low_balance_threshold = (
            0.1  # Порог для отображения минимальной суммы активов in $
        )
        self._transaction_processor = TransactionProcessor(self)
        self._calculator = PortfolioCalculator(self)

    async def make_portfolio(self, transactions: list[TransactionRead]):
        self._transaction_processor.process_transactions(transactions)
        await self._calculator.calculate()

    @property
    def assets(self) -> dict[int, CryptoAsset]:
        assets = self._hide_assets_with_low_balance()
        return assets.values()

    def _hide_assets_with_low_balance(self) -> dict[int, CryptoAsset]:
        return {
            token_id: asset
            for token_id, asset in self._assets.items()
            if asset.balance >= self._low_balance_threshold
        }
