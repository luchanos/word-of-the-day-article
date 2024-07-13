import asyncio

import httpx
import pytest
import settings
from app.application import create_minimal_app
from app.context import FastAPIWithContext
from app.db import RedisClient
from app.openai_client import AsyncOpenAIClient
from app.wordsmith import WordsmithClient


@pytest.fixture(scope="session")
def event_loop():
    """
    For proper loop execution in scope="session".
    https://github.com/tortoise/tortoise-orm/issues/638#issuecomment-830124562
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(autouse=True)
# def block_httpx(monkeypatch):
#     import httpx
#
#     def raise_runtime_error(*args, **kwargs):
#         raise RuntimeError("External calls are blocked during testing")
#
#     monkeypatch.setattr(httpx.AsyncClient, "get", raise_runtime_error)
#     monkeypatch.setattr(httpx.AsyncClient, "post", raise_runtime_error)
#     monkeypatch.setattr(httpx.AsyncClient, "put", raise_runtime_error)
#     monkeypatch.setattr(httpx.AsyncClient, "delete", raise_runtime_error)


@pytest.fixture(scope="session")
async def redis_client() -> RedisClient:
    client = RedisClient(host=settings.REDIS_TEST_HOST, port=settings.REDIS_TEST_PORT)
    yield client
    await client.close()


@pytest.fixture(scope="function", autouse=True)
async def clean_redis():
    client = RedisClient(host=settings.REDIS_TEST_HOST, port=settings.REDIS_TEST_PORT)
    await client.flushdb()


@pytest.fixture(scope="session")
async def openai_client() -> AsyncOpenAIClient:
    client = AsyncOpenAIClient(api_key="test_openai_key")
    yield client


@pytest.fixture(scope="session")
async def wordsmith_client() -> WordsmithClient:
    client = WordsmithClient()
    yield client


@pytest.fixture
async def test_app(redis_client, wordsmith_client) -> FastAPIWithContext:
    app = create_minimal_app()

    app.wordsmith_client = wordsmith_client,
    app.openai_client = AsyncOpenAIClient(settings.OPENAI_TEST_API_KEY),
    app.redis_client = redis_client

    yield app


@pytest.fixture
async def test_cli(test_app) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=test_app, base_url="http://test") as test_client:
        yield test_client
