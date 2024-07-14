import datetime
import json


class ArticleCache:
    def __init__(self, *args, **kwargs):
        self.cache = {}  # expiry dict or Ordered dict with limits

    async def cache_article(self, header: str, article: str) -> None:
        key = str(datetime.date.today())
        value = json.dumps({"header": header, "body": article})
        self.cache[key] = value

    async def get_cached_article(self) -> dict | None:
        key = str(datetime.date.today())
        cached_data = self.cache.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None
