import asyncio
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Sequence

import pandas as pd

from base.base_model import CryptoTransaction
from modules.cryptos.crypto.coin_geko_API import CoinGekoAPI


class TimePeriod(Enum):
    DAILY = ("daily", 1, 15 * 60, "15min")  # 15 min
    WEEKLY = ("weekly", 8, 1 * 60 * 60, "h")  # 1 hour
    MONTHLY = ("monthly", 31, 6 * 60 * 60, "6h")  # 6 hour
    YEARLY = ("yearly", 365, 24 * 60 * 60, "24h")  # 24 hour

    def __new__(cls, value, days_ago, divider, time_step):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.days_ago = days_ago
        obj.divider = divider
        obj.time_step = time_step
        return obj


class GraphMaker1:
    def __init__(self, transactions: list[CryptoTransaction], period: TimePeriod):
        self._transactions = transactions
        self._period = period
        self._tokens = None
        self._dataframe: pd.DataFrame = None

    async def count_assets_cost(self):
        self._process_transactions()
        self._set_unique_tokens()
        prices = self._get_prices()
        self._merge_dataframe_and_prices(prices)
        self._calculate_total_cost()
        print(self._dataframe)

    async def _get_prices(self):
        price_tasks = [self._get_token_prices(token) for token in self._tokens]
        prices = await asyncio.gather(*price_tasks)
        return prices

    def _calculate_total_cost(self):
        self._dataframe["total_value"] = 0

        for token in self._tokens:
            quantity_col = token
            price_col = f"{token}_price"

            quantity = self._dataframe[token].fillna(0)
            price = self._dataframe[f"{token}_price"].fillna(0)

            if (
                quantity_col in self._dataframe.columns
                and price_col in self._dataframe.columns
            ):
                self._dataframe["total_value"] += quantity * price
                self._dataframe["total_value"] += quantity * price

        json_data = self._dataframe["total_value"].to_json(orient="index")

        print("JSON_DATA", json_data)

    async def _get_token_prices(self, token: str) -> dict:
        request = await CoinGekoAPI.get_token_price_history(
            token, self._period.days_ago
        )
        prices = self._process_apis_timestamps_and_prices(request["prices"])
        print(prices)
        return {token: prices}

    def _process_apis_timestamps_and_prices(self, prices: list) -> Sequence[Sequence]:
        formatted_values = []
        for raw_timestamp, price in prices:
            timestamp_without_ms = int(raw_timestamp / 1000)
            timestamp = (
                timestamp_without_ms // self._period.divider * self._period.divider
            )
            formatted_values.append((timestamp, price))
        return formatted_values

    def _process_transactions(self):
        self._dataframe = pd.DataFrame(index=self._make_timestamp_axis())
        for transaction in self._transactions:
            operation_time: datetime.timestamp = transaction["created_at"]
            amount = transaction["amount"]
            asset = transaction["asset"]

            nearest_timestamp = self._round_timestamp(operation_time)

            if nearest_timestamp in self._dataframe.index:
                if asset in self._dataframe.columns:
                    self._dataframe.loc[
                        self._dataframe.index >= nearest_timestamp, asset
                    ] += amount
                else:
                    self._dataframe.at[nearest_timestamp:, asset] = amount
                    self._dataframe.at[nearest_timestamp:, f"{asset}_price"] = 0

    def _make_timestamp_axis(self) -> pd.date_range:
        dt_now = self._round_datetime(datetime.now(timezone.utc))
        start_date = dt_now - timedelta(days=self._period.days_ago)
        date_range = pd.date_range(
            start=start_date, end=dt_now, freq=self._period.time_step
        )
        unix_timestamps = date_range.astype("int64") // 10**9
        print("CLEAR DF", unix_timestamps)
        return unix_timestamps

    def _round_datetime(self, dt: datetime) -> datetime:
        hour, minute = dt.hour, dt.minute
        if self._period == TimePeriod.DAILY:
            minute = (dt.minute // 15) * 15
        elif self._period == TimePeriod.WEEKLY:
            minute = 0
        elif self._period == TimePeriod.MONTHLY:
            minute, hour = 0, (dt.hour // 6) * 6
        else:
            minute, hour = 0, 0
        return dt.replace(hour=hour, minute=minute, second=0, microsecond=0)

    def _set_unique_tokens(self):
        columns = self._dataframe.columns.unique()
        self._tokens = [column for column in columns if "_price" not in column]

    def _merge_dataframe_and_prices(self, prices: list[dict]):
        for token_info in prices:
            for token_name, timestamp_and_price in token_info.items():
                for timestamp, price in timestamp_and_price:
                    self._dataframe.loc[timestamp, f"{token_name}_price"] = price
                    self._dataframe = self._dataframe.interpolate(method="linear")

        if self._dataframe.iloc[0].isnull().any():
            self._dataframe.iloc[0] = self._dataframe.iloc[1]
        if self._dataframe.iloc[-1].isnull().any():
            self._dataframe.iloc[-1] = self._dataframe.iloc[-2]

    def _round_timestamp(self, timestamp: int) -> int:
        return timestamp // self._period.divider * self._period.divider


class DatetimeRounder:
    @staticmethod
    def round_datetime(dt_value: datetime, period: TimePeriod) -> datetime:
        hour, minute = dt_value.hour, dt_value.minute
        if period == TimePeriod.DAILY:
            minute = (dt_value.minute // 15) * 15
        elif period == TimePeriod.WEEKLY:
            minute = 0
        elif period == TimePeriod.MONTHLY:
            minute, hour = 0, (dt_value.hour // 6) * 6
        else:
            minute, hour = 0, 0
        return dt_value.replace(hour=hour, minute=minute, second=0, microsecond=0)


class DataFrameMaker:
    def __init__(self, period: TimePeriod):
        self._period = period

    def make_dataframe(self) -> pd.date_range:
        dt_now = DatetimeRounder.round_datetime(
            dt_value=datetime.now(timezone.utc), period=self._period
        )
        start_date = dt_now - timedelta(days=self._period.days_ago)

        date_range = pd.date_range(
            start=start_date, end=dt_now, freq=self._period.time_step
        )
        unix_timestamps = date_range.astype("int64") // 10**9
        dataframe = pd.DataFrame(index=unix_timestamps)
        print("TYPE DF", type(dataframe))
        print("CLEAR DF", dataframe)
        return dataframe


class TransactionProcessor:
    def __init__(
        self,
        transactions: list[CryptoTransaction],
        period: TimePeriod,
        dataframe: pd.DataFrame | None = None,
    ):
        self._transactions = transactions
        self._period = period
        self._dataframe = dataframe

    @property
    def dataframe(self):
        return self._dataframe

    def add_transactions_in_df(self, dataframe: pd.DataFrame):
        self._dataframe = dataframe
        for transaction in self._transactions:
            self._process_transaction(transaction)

    def _process_transaction(self, transaction):
        operation_time = transaction["created_at"]
        amount = transaction["amount"]
        asset = transaction["asset"]
        nearest_timestamp = self._round_timestamp(operation_time)

        if nearest_timestamp in self._dataframe.index:
            if asset in self._dataframe.columns:
                self._dataframe.loc[
                    self._dataframe.index >= nearest_timestamp, asset
                ] += amount
            else:
                self._dataframe.at[nearest_timestamp:, asset] = amount
                self._dataframe.at[nearest_timestamp:, f"{asset}_price"] = 0

    def _round_timestamp(self, timestamp: int) -> int:
        return timestamp // self._period.divider * self._period.divider

    def add_price_in_df(self, prices: Sequence[dict]):
        for token_info in prices:
            for token_name, timestamp_and_price in token_info.items():
                for timestamp, price in timestamp_and_price:
                    self._dataframe.loc[timestamp, f"{token_name}_price"] = price
                    self._dataframe = self._dataframe.interpolate(method="linear")

        if self._dataframe.iloc[0].isnull().any():
            self._dataframe.iloc[0] = self._dataframe.iloc[1]
        if self._dataframe.iloc[-1].isnull().any():
            self._dataframe.iloc[-1] = self._dataframe.iloc[-2]


class PriceFetcher:
    def __init__(self, period: TimePeriod):
        self._period = period

    async def fetch_prices(
        self, dataframe: pd.DataFrame, tokens: list[str]
    ) -> Sequence[dict]:
        price_tasks = [self._get_token_prices(token) for token in tokens]
        return await asyncio.gather(*price_tasks)

    async def _get_token_prices(self, token: str) -> dict:
        request = await CoinGekoAPI.get_token_price_history(
            token, self._period.days_ago
        )
        prices = self._format_timestamps(request["prices"])
        return {token: prices}

    def _format_timestamps(self, prices: list[list]) -> Sequence[Sequence]:
        formatted_values = []
        for raw_timestamp, price in prices:
            timestamp_without_ms = int(raw_timestamp / 1000)
            timestamp = (
                timestamp_without_ms // self._period.divider * self._period.divider
            )
            formatted_values.append((timestamp, price))
        return formatted_values


class CostCalculator:
    @staticmethod
    def calculate_total_cost(dataframe: pd.DataFrame, tokens: list[str]):
        dataframe["total_value"] = 0

        for token in tokens:
            quantity_col = token
            price_col = f"{token}_price"

            quantity = dataframe[token].fillna(0)
            price = dataframe[f"{token}_price"].fillna(0)

            if quantity_col in dataframe.columns and price_col in dataframe.columns:
                dataframe["total_value"] += quantity * price
                dataframe["total_value"] += quantity * price

        json_data = dataframe["total_value"].to_json(orient="index")

        print("JSON_DATA", json_data)


class GraphMaker:
    def __init__(self, transactions: list[CryptoTransaction], period: TimePeriod):
        self.df_maker = DataFrameMaker(period)
        self.processor = TransactionProcessor(transactions, period)
        self.price_fetcher = PriceFetcher(period)
        self.calculator = CostCalculator

    async def count_assets_cost(self):
        base_df: pd.DataFrame = self.df_maker.make_dataframe()
        self.processor.add_transactions_in_df(base_df)

        tokens = self._extract_tokens(self.processor.dataframe)
        prices = await self.price_fetcher.fetch_prices(self.processor.dataframe, tokens)
        self.processor.add_price_in_df(prices)

        self.calculator.calculate_total_cost(self.processor.dataframe, tokens)
        print(self.processor.dataframe)

    def _extract_tokens(self, dataframe: pd.DataFrame):
        columns = dataframe.columns.unique()
        return [column for column in columns if "_price" not in column]


transactions = [
    {"created_at": 1725158622, "amount": 0.1, "asset": "bitcoin"},
    {"created_at": 1725446622, "amount": 0.1, "asset": "ethereum"},
    {"created_at": 1725360222, "amount": 0.2, "asset": "ethereum"},
    {"created_at": 1725342222, "amount": 0.05, "asset": "ethereum"},
]


start = datetime.now()
# asyncio.run(GraphMaker1(transactions, TimePeriod.DAILY).count_assets_cost())


asyncio.run(GraphMaker(transactions, TimePeriod.WEEKLY).count_assets_cost())


print(datetime.now() - start)
