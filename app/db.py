import json
import datetime
import redis.asyncio as redis
import asyncio


class RedisClient:
    def __init__(self, host: str, port: int = 6379, db: int = 0, max_connections: int = 10):
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            max_connections=max_connections,
            decode_responses=True
        )
        self.client = redis.Redis(connection_pool=self.pool)

    async def cache_article(self, header: str, article: str):
        await self.client.set(str(datetime.date.today()), json.dumps({"header": header, "body": article}))

    async def get_cached_article(self):
        return await self.client.get(str(datetime.date.today()))

    async def close(self):
        await self.client.connection_pool.disconnect()


# Example usage
async def main():
    redis_client = RedisClient(host="0.0.0.0", port=6379, max_connections=10)
    await redis_client.cache_article("example_word", article="test")
    word = await redis_client.get_cached_article()
    print(word)
    await redis_client.close()

if __name__ == "__main__":
    asyncio.run(main())
