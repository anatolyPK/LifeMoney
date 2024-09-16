class MathOperation:
    @staticmethod
    def get_new_average_price(
            old_average_price: float, new_price: float, old_size: float, new_buy_size: float
    ) -> float:
        """Рассчитывает новую среднюю стоимость актива"""

        return (old_size * old_average_price + new_buy_size * new_price) / (new_buy_size + old_size)

    @classmethod
    def get_profits(
            cls, average_price_buy: float, balance: float
    ) -> tuple[float, float]:
        profit_in_currency = cls._count_currency_profit(average_price_buy, balance)
        profit_in_percent = cls._count_percent_profit(average_price_buy, balance)
        return profit_in_currency, profit_in_percent

    @staticmethod
    def _count_currency_profit(start_price: float, now_price: float) -> float:
        return now_price - start_price

    @staticmethod
    def _count_percent_profit(start_price: float, now_price: float) -> float:
        if start_price == 0:
            return 0
        """Считает изменение стоимости с start_price до now_price актива в процентах"""
        return ((now_price - start_price) / start_price) * 100

    @staticmethod
    def get_asset_percent_of_portfolio(assets_balance: float, portfolio_balance: float):
        return assets_balance / portfolio_balance * 100 if portfolio_balance != 0 else 0
