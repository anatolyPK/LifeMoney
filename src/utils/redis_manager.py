import redis.asyncio as redis


class AsyncRedis:
    def __init__(self, host='localhost', port=6379):
        self._redis = None
        self._host = host
        self._port = port

    async def __aenter__(self):
        self._redis = redis.Redis(
            host=self._host,
            port=self._port,
            decode_responses=True)
        await self._redis.ping()
        return self._redis

    async def __aexit__(self, exc_type, exc, tb):
        if self._redis:
            await self._redis.close()
