import redis.asyncio as redis


class RedisClient:
    def __init__(self, host: str, port: int = 6379, db: int = 0, max_connections: int = 10):
        self._pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            max_connections=max_connections,
            decode_responses=True
        )
        self.client = redis.Redis(connection_pool=self._pool)

    async def set(self, key: str, value: str):
        await self.client.set(key, value)

    async def get(self, key: str):
        return await self.client.get(key)

    async def flushdb(self):
        await self.client.flushdb()

    async def close(self):
        await self.client.connection_pool.disconnect()
