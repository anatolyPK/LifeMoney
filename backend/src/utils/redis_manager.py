import redis.asyncio as redis
from collections import deque

from backend.src.core.config.project import settings


class AsyncRedis:
    def __init__(self):
        self._pools = deque()
        self._host = settings.redis.REDIS_HOST
        self._port = settings.redis.REDIS_PORT
        self._max_connections = settings.redis.REDIS_MAX_CONNECTIONS

    async def connect(self):
        for _ in range(self._max_connections):
            pool = redis.ConnectionPool(
                host=self._host,
                port=self._port,
                max_connections=self._max_connections,
                decode_responses=True,
            )
            self._pools.append(pool)
        print("CONNECT!")

    async def get_client(self):
        if not self._pools:
            raise Exception("No available connection pools")
        pool = self._pools.popleft()
        return redis.Redis(connection_pool=pool), pool

    def _return_pool(self, pool):
        self._pools.append(pool)

    async def set(self, key, value):
        client, pool = await self.get_client()
        try:
            await client.set(key, value)
        finally:
            self._return_pool(pool)

    async def get(self, key):
        client, pool = await self.get_client()
        try:
            return await client.get(key)
        finally:
            self._return_pool(pool)

    async def close(self):
        while self._pools:
            pool = self._pools.popleft()
            await pool.disconnect()


redis_client = AsyncRedis()
