from backend.src.modules.common.math import MathOperation
from backend.src.modules.cryptos.schemas import TokenSchema


class BaseAsset:
    def __init__(
        self, asset_info: TokenSchema, quantity: float, average_price_buy: float
    ):
        self._asset_info = asset_info
        self._quantity = quantity
        self._average_price_buy = average_price_buy

        self._balance = 0
        self._current_price = 0
        self._profit_in_currency = 0
        self._profit_in_percent = 0
        self._percent_of_portfolio = 0

    @property
    def average_price_buy(self):
        return self._average_price_buy

    @average_price_buy.setter
    def average_price_buy(self, price: float, quantity: float):
        self._average_price_buy = MathOperation.get_new_average_price(
            old_average_price=self.average_price_buy,
            new_price=price,
            old_size=self._quantity,
            new_buy_size=quantity,
        )

    # @property
    # def
    #
    # @property
    # def
    #
    # @property
    # def
    #
    # @property
    # def
