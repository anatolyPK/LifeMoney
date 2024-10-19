import asyncio
from datetime import datetime, timedelta

from backend.src.modules.common.redis_storage import redis_manager, USDRUB_FIGI
from backend.src.modules.stocks.services import stock_service
from backend.src.modules.stocks.tinkoff_api import TinkoffAPI
from backend.src.modules.stocks.utils import convert_tinkoff_money_in_currency, convert_to_timestamp
from backend.src.utils.time_manager import timing_decorator

DATE_2020_1_1 = 1577836800

@timing_decorator
async def set_actual_stock_price():
    prices = await stock_service.get_assets_price()

    for asset in prices["lastPrices"]:
        key = asset["figi"].lower()
        price = str(convert_tinkoff_money_in_currency(asset.get("price")))
        await redis_manager.set_current_price(key, price)


async def get_candles_yearly(figi: str = USDRUB_FIGI, start_timestamp: int = DATE_2020_1_1):
    start_date = datetime.fromtimestamp(start_timestamp)
    end_date = datetime.utcnow()
    interval = "5"

    tasks = []
    while start_date < end_date:
        next_date = start_date + timedelta(days=365)
        to_date = min(next_date, end_date)

        from_str = start_date.isoformat() + "Z"
        to_str = to_date.isoformat() + "Z"

        tasks.append(TinkoffAPI.get_candles(figi, from_str, to_str, interval))
        start_date = next_date

    results = []
    for completed in asyncio.as_completed(tasks):
        candles = await completed
        res = await _set_price_in_redis(candles, figi)
        results.append(res)
    return results

async def _set_price_in_redis(candles: dict, figi: str):
    for candle in candles['candles']:
        await redis_manager.set_historical_price(
            item_id=figi,
            price=convert_tinkoff_money_in_currency(candle['close']),
            timestamp=convert_to_timestamp(candle['time'])
        )