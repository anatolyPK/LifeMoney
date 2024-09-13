from utils.redis_manager import redis_client


class RedisCryptoKeys:
    @staticmethod
    def _get_current_price_key(item_id) -> str:
        return f"prices:current:{item_id}"

    @staticmethod
    def _get_historical_price_key(item_id, timestamp) -> str:
        return f"prices:historical:daily:{item_id}:{timestamp}"


class RedisCryptoManager(RedisCryptoKeys):
    def __init__(self, _redis_client):
        self._client = _redis_client

    async def set_current_price(self, item_id, price):
        key = self._get_current_price_key(item_id)
        await self._client.set(key, price)

    async def get_current_price(self, item_id) -> float:
        key = self._get_current_price_key(item_id.lower())
        price: str = await self._client.get(key)
        return float(price) if price else 0

    async def set_historical_price(self, item_id, price, timestamp):
        key = self._get_historical_price_key(item_id, timestamp)
        await self._client.set(key, price)

    async def get_historical_price(self, item_id, timestamp):
        key = self._get_historical_price_key(item_id, timestamp)
        await self._client.get(key)


redis_manager = RedisCryptoManager(redis_client)
