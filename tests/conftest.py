import asyncio

import httpx
import pytest
import settings
from app.application import create_minimal_app
from app.context import FastAPIWithContext
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


@pytest.fixture(scope="session")
async def openai_client() -> AsyncOpenAIClient:
    client = AsyncOpenAIClient(api_key="test_openai_key")
    yield client


@pytest.fixture(scope="session")
async def wordsmith_client() -> WordsmithClient:
    client = WordsmithClient()
    yield client


@pytest.fixture
async def test_app(wordsmith_client) -> FastAPIWithContext:
    app = create_minimal_app()

    app.wordsmith_client = wordsmith_client
    app.openai_client = AsyncOpenAIClient(settings.OPENAI_TEST_API_KEY)

    yield app


@pytest.fixture
async def test_cli(test_app) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=test_app, base_url="http://test") as test_client:
        yield test_client
