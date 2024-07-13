import asyncio
from unittest.mock import AsyncMock

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
def openai_client() -> AsyncMock:
    client = AsyncMock(spec=AsyncOpenAIClient)
    client.api_key = settings.OPENAI_TEST_API_KEY
    return client


@pytest.fixture(scope="session")
def wordsmith_client() -> AsyncMock:
    client = AsyncMock(spec=WordsmithClient)
    return client


@pytest.fixture
async def test_app(wordsmith_client, openai_client) -> FastAPIWithContext:
    app = create_minimal_app()

    app.wordsmith_client = wordsmith_client
    app.openai_client = openai_client

    yield app


@pytest.fixture
async def test_cli(test_app) -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=test_app, base_url="http://test") as test_client:
        yield test_client
