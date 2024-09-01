from typing import List

from src.modules.cryptos.schemas import CryptoAsset, TransactionRead

stablecoins = ['usdt', 'usdc']
fiat_currencies = ['rub', 'usd']


class MathOperation:
    @staticmethod
    def get_new_average_price(old_average_price: float,
                              new_price: float,
                              old_size: float,
                              new_buy_size: float) -> float:
        """Рассчитывает новую среднюю стоимость актива"""
        return (old_size * old_average_price + new_buy_size * new_price) / (new_buy_size + old_size)

    @classmethod
    def get_profits(cls, average_price_buy: float, balance: float) -> tuple[float, float]:
        profit_in_currency = cls._count_currency_profit(average_price_buy, balance)
        profit_in_percent = cls._count_percent_profit(average_price_buy, balance)
        return profit_in_currency, profit_in_percent

    @staticmethod
    def _count_currency_profit(start_price: float, now_price: float) -> float:
        return now_price - start_price

    @staticmethod
    def _count_percent_profit(start_price: float,
                              now_price: float) -> float:
        """Считает изменение стоимости с start_price до now_price актива в процентах"""
        return ((now_price - start_price) / start_price) * 100


class TransactionManager:
    @staticmethod
    async def _is_input_transaction(transaction: TransactionRead):
        return (
                transaction.token_2.lower() in fiat_currencies and
                transaction.is_buy_or_sell
        )

    @staticmethod
    async def _is_output_transaction(transaction: TransactionRead):
        return (
                transaction.token_2.lower() in fiat_currencies and
                not transaction.is_buy_or_sell
        )


class CryptoPortfolioMaker(TransactionManager):
    def __init__(self):
        self.balance = 0

        self.assets: List[CryptoAsset] = []

    def make_portfolio(self, transactions: list[TransactionRead]):
        for transaction in transactions:
            self._process_transaction(transaction)
        self.recalculate_portfolio()
        return self.assets

    def _process_buy(self, token: str, quantity: float, price_in_usd: float):
        asset_index = self._get_asset_index_in_assets(token=token)
        self._summarize_token(assets_ind=asset_index, quantity=quantity, price=price_in_usd)

    def _process_sell(self, token: str, quantity: float, price_in_usd: float):
        asset_index = self._get_asset_index_in_assets(token=token, may_be_null=True)
        if asset_index is not None:
            self._subtract_token(assets_ind=asset_index, quantity=quantity * (1 / price_in_usd))

    def _process_transaction(self, transaction: TransactionRead):
        if transaction.is_buy_or_sell:
            self._process_buy(
                token=transaction.token_1,
                quantity=transaction.quantity,
                              price_in_usd=transaction.price_in_usd
            )
            self._process_sell(
                token=transaction.token_2,
                quantity=transaction.quantity,
                               price_in_usd=transaction.price_in_usd
            )
        else:
            self._process_sell(
                token=transaction.token_1,
                quantity=transaction.quantity,
                               price_in_usd=transaction.price_in_usd
            )
            self._process_buy(
                token=transaction.token_2,
                quantity=transaction.quantity,
                              price_in_usd=transaction.price_in_usd
            )

    def _get_asset_index_in_assets(self, token: str, may_be_null: bool = False):
        assets_ind = self._check_asset_exist_in_portfolio(token)
        if assets_ind is None and not may_be_null:
            assets_ind = self._create_asset(token=token)
        return assets_ind

    def _check_asset_exist_in_portfolio(self, token: str) -> int | None:
        """Если токен в портфеле, возвращает индекс актива в массиве активов портфеля.
        Если токена нет - возвращает None"""
        for ind, crypto_asset in enumerate(self.assets):
            if token == crypto_asset.token:
                return ind
        return

    def _summarize_token(self, assets_ind: int, quantity: float, price: float):
        self.assets[assets_ind].average_price_buy = MathOperation.get_new_average_price(
            old_average_price=self.assets[assets_ind].average_price_buy,
            new_price=price,
            old_size=self.assets[assets_ind].quantity,
            new_buy_size=quantity
        )
        self.assets[assets_ind].quantity1 += quantity

    def _subtract_token(self, assets_ind: int, quantity: float):
        self.assets[assets_ind].quantity += quantity
        if self.assets[assets_ind].quantity < 0:
            self.assets[assets_ind].quantity = 0

    def _create_asset(self, token: str) -> int:
        """Добавляет актив в портфель пользователя.
        Возвращает индекс актива в массиве активов пользователя"""
        asset = CryptoAsset(token=token)
        self.assets.append(asset)
        return len(self.assets) - 1

    def recalculate_portfolio(self):
        for asset in self.assets:
            asset.current_price = 30000  # REDIS
            asset.balance = asset.quantity * asset.current_price
            self.balance += asset.balance
            asset.profit_in_currency, asset.profit_in_percent = MathOperation.get_profits(
                asset.average_price_buy * asset.quantity,
                asset.balance
            )

        for asset in self.assets:
            asset.percent_of_portfolio = asset.balance / self.balance
