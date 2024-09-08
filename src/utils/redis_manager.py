import redis.asyncio as redis
from collections import deque


class AsyncRedis:
    def __init__(self, host="redis", port=6379, max_connections=10):
        self._pools = deque()
        self._host = host
        self._port = port
        self._max_connections = max_connections

    async def connect(self):
        for _ in range(self._max_connections):
            pool = redis.ConnectionPool(
                host=self._host,
                port=self._port,
                max_connections=self._max_connections,
                decode_responses=True,
            )
            self._pools.append(pool)
        print('CONNECT!')

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
