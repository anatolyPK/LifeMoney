from src.crypto.utils.coin_market_cup_API import CoinMarketCupAPI
from src.utils.redis_manager import AsyncRedis
from src.utils.time_manager import timing_decorator


@timing_decorator
async def set_actual_crypto_price():
    prices_from_api = await CoinMarketCupAPI.get_cryptocurrency_listings(5000)
    async with AsyncRedis() as redis_client:
        for crypto in prices_from_api['data']:
            key = crypto['symbol']
            price = str(crypto['quote']['USD']['price'])
            await redis_client.set(key, price)


