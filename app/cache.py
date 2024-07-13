import datetime
import json

from app.db import RedisClient


class ArticleCacheV2:
    def __init__(self, *args, **kwargs):
        self.cache = {}

    async def cache_article(self, header: str, article: str):
        key = str(datetime.date.today())
        value = json.dumps({"header": header, "body": article})
        self.cache[key] = value

    async def get_cached_article(self):
        key = str(datetime.date.today())
        cached_data = self.cache.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None


class ArticleCache:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    async def cache_article(self, header: str, article: str):
        key = str(datetime.date.today())
        value = json.dumps({"header": header, "body": article})
        await self.redis_client.set(key, value)

    async def get_cached_article(self):
        key = str(datetime.date.today())
        cached_data = await self.redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None
