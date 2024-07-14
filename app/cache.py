import datetime
import json
import time
from collections import OrderedDict


class ArticleCache:
    def __init__(self, ttl: int = 60 * 60 * 24, maxsize: int = 128):
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache = OrderedDict()

    def _is_expired(self, entry: dict) -> bool:
        return time.time() - entry['time'] > self.ttl

    def _evict_expired(self):
        keys_to_delete = [
            key for key, entry in self.cache.items() if self._is_expired(entry)
        ]
        for key in keys_to_delete:
            del self.cache[key]

    def _evict_if_needed(self):
        while len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)

    async def cache_article(self, header: str, article: str) -> None:
        self._evict_expired()
        key = str(datetime.date.today())
        value = json.dumps({"header": header, "body": article})
        self.cache[key] = {'value': value, 'time': time.time()}
        self._evict_if_needed()

    async def get_cached_article(self) -> dict | None:
        self._evict_expired()
        key = str(datetime.date.today())
        entry = self.cache.get(key)
        if entry and not self._is_expired(entry):
            return json.loads(entry['value'])
        return None
