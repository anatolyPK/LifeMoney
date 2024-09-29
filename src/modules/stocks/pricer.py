
from modules.cryptos.crypto.coin_market_cup_API import CoinMarketCupAPI
from modules.common.redis_storage import redis_manager
from modules.stocks.services import stock_service
from modules.stocks.tinkoff_api import TinkoffAPI
from modules.stocks.utils import convert_tinkoff_money_in_currency
from src.utils.time_manager import timing_decorator


@timing_decorator
async def set_actual_stock_price():
    prices = await stock_service.get_assets_price()
    for asset in prices["lastPrices"]:
        key = asset["figi"].lower()
        price = str(convert_tinkoff_money_in_currency(asset.get('price')))
        await redis_manager.set_current_price(key, price)

