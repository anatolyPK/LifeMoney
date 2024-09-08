from modules.cryptos.crypto.coin_market_cup_API import CoinMarketCupAPI
from modules.cryptos.crypto.crypto_storage import redis_manager
from src.utils.time_manager import timing_decorator


@timing_decorator
async def set_actual_crypto_price():
    prices_from_api = await CoinMarketCupAPI.get_cryptocurrency_listings(4000)
    for crypto in prices_from_api["data"]:
        key = crypto["symbol"]
        price = str(crypto["quote"]["USD"]["price"])
        await redis_manager.set_current_price(key, price)

@timing_decorator
async def set_actual_crypto_price_no_redis():
    prices_from_api = await CoinMarketCupAPI.get_cryptocurrency_listings(4000)
    for crypto in prices_from_api["data"]:
        key = crypto["symbol"]
        price = str(crypto["quote"]["USD"]["price"])
        # await redis_manager.set_current_price(key, price)
