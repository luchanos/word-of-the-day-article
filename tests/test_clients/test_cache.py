import asyncio
import datetime
import json

from app.cache import ArticleCache


async def test_cache_article():
    cache = ArticleCache(ttl=60, maxsize=128)
    await cache.cache_article("Test Header", "Test Body")

    key = str(datetime.date.today())
    cached_value = cache.cache.get(key)

    assert cached_value is not None
    assert json.loads(cached_value['value']) == {
        "header": "Test Header",
        "body": "Test Body",
    }


async def test_get_cached_article():
    cache = ArticleCache(ttl=60, maxsize=128)
    await cache.cache_article("Test Header", "Test Body")

    article = await cache.get_cached_article()

    assert article is not None
    assert article == {"header": "Test Header", "body": "Test Body"}


async def test_expired_article():
    cache = ArticleCache(ttl=1, maxsize=128)
    await cache.cache_article("Test Header", "Test Body")

    await asyncio.sleep(2)

    article = await cache.get_cached_article()

    assert article is None


async def test_cache_size_limit():
    cache = ArticleCache(ttl=60, maxsize=2)
    await cache.cache_article("Test Header 1", "Test Body 1")
    await cache.cache_article("Test Header 2", "Test Body 2")
    await cache.cache_article("Test Header 3", "Test Body 3")

    key1 = str(datetime.date.today())
    cached_article_1 = cache.cache.get(key1)
    assert cached_article_1 is not None
    assert json.loads(cached_article_1['value']) == {
        "header": "Test Header 3",
        "body": "Test Body 3",
    }

    await asyncio.sleep(1)

    key2 = str(datetime.date.today() - datetime.timedelta(days=1))
    cached_article_2 = cache.cache.get(key2)
    assert cached_article_2 is None


async def test_cache_multiple_articles():
    cache = ArticleCache(ttl=60, maxsize=128)
    await cache.cache_article("Test Header 1", "Test Body 1")

    key_today = str(datetime.date.today())
    article_today = await cache.get_cached_article()
    assert article_today == {"header": "Test Header 1", "body": "Test Body 1"}

    await asyncio.sleep(1)

    await cache.cache_article("Test Header 2", "Test Body 2")
    article_today_2 = await cache.get_cached_article()
    assert article_today_2 == {"header": "Test Header 2", "body": "Test Body 2"}

    cached_value_today = cache.cache.get(key_today)
    assert json.loads(cached_value_today['value']) == {
        "header": "Test Header 2",
        "body": "Test Body 2",
    }
