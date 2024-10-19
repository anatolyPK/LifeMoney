from backend.src.modules.cryptos.crypto.coin_market_cup_API import CoinMarketCupAPI
from backend.src.modules.common.redis_storage import redis_manager
from backend.src.utils.time_manager import timing_decorator


@timing_decorator
async def set_actual_crypto_price():
    prices_from_api = await CoinMarketCupAPI.get_cryptocurrency_listings(300)
    for crypto in prices_from_api["data"]:
        key = crypto["symbol"].lower()
        price = str(crypto["quote"]["USD"]["price"])
        await redis_manager.set_current_price(key, price)

