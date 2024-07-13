from http import HTTPStatus
from unittest.mock import AsyncMock

from api.articles.service import GetArticleHandler
from app.cache import ArticleCache
from app.context import FastAPIWithContext
from app.openai_client import AsyncOpenAIClient
import httpx

from app.wordsmith import WordsmithClient
import pytest


@pytest.fixture
def mock_app(mock_cache, mock_wordsmith_client, mock_openai_client):
    app = FastAPIWithContext(
        wordsmith_client=mock_wordsmith_client,
        openai_client=mock_openai_client,
    )
    app.cache = {"article": mock_cache}
    return app


async def test_get_article_flow(test_cli, mock_app):
    test_header = "Generated Header"
    test_body = "Test Content"
    mock_response_json = {
        "choices": [{
            "message": {
                "content": '{"header": "%s", "body": "%s"}' % (test_header, test_body)
            }
        }]
    }
    WordsmithClient.get_awad = AsyncMock(return_value='psychrophobia')
    mock_openai_response_content = httpx.Response(
        status_code=200,
        json=mock_response_json
    )
    AsyncOpenAIClient.make_prompt_request = AsyncMock(return_value=mock_openai_response_content)

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["header"] == test_header
    assert data["body"] == test_body


async def test_get_article_from_cache(test_cli, mock_app):
    test_header = "Test Header"
    test_body = "Test Body"
    ArticleCache.get_cached_article = AsyncMock(
        return_value={"actual_date": "2024-01-01", "header": test_header, "body": test_body})
    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["header"] == test_header
    assert data["body"] == test_body
    ArticleCache.get_cached_article.assert_called_once()


async def test_get_article_generate_and_cache(test_cli, mock_app):
    ArticleCache.get_cached_article = AsyncMock(return_value=None)
    ArticleCache.cache_article = AsyncMock()
    WordsmithClient.get_awad = AsyncMock(return_value='psychrophobia')

    test_header = "Generated Header"
    test_body = "Generated Body"
    mock_response_json = {
        "choices": [{
            "message": {
                "content": '{"header": "%s", "body": "%s"}' % (test_header, test_body)
            }
        }]
    }
    mock_openai_response_content = httpx.Response(
        status_code=200,
        json=mock_response_json
    )
    AsyncOpenAIClient.make_prompt_request = AsyncMock(return_value=mock_openai_response_content)

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["header"] == test_header
    assert data["body"] == test_body

    ArticleCache.get_cached_article.assert_called_once()
    ArticleCache.cache_article.assert_called_once_with(
        header=test_header,
        article=test_body
    )
    WordsmithClient.get_awad.assert_called_once()
    AsyncOpenAIClient.make_prompt_request.assert_called_once_with(
        prompt=GetArticleHandler.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(awad="psychrophobia"))
