import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from api.articles.service import GetArticleHandler

from api.articles.model import GetArticleResponseModel
from app.context import FastAPIWithContext


@pytest.fixture
def mock_cache():
    return MagicMock()


@pytest.fixture
def mock_wordsmith_client():
    return AsyncMock()


@pytest.fixture
def mock_openai_client():
    return AsyncMock()


async def test_get_article_from_cache(test_cli, mock_cache):
    mock_cache.get_cached_article.return_value = {
        "header": "Test Header",
        "body": "Test Body"
    }

    handler = GetArticleHandler()
    response = await test_cli.get("/api/v1/articles")

    assert response == GetArticleResponseModel(
        actual_date=date.today(),
        header="Test Header",
        body="Test Body"
    )
    mock_cache.get_cached_article.assert_called_once()

#
# async def test_get_article_generate_and_cache(mock_app, mock_cache, mock_wordsmith_client, mock_openai_client):
#     mock_cache.get_cached_article.return_value = None
#     mock_wordsmith_client.get_awad.return_value = "test_word"
#     mock_openai_client.make_prompt_request.return_value = MagicMock(json=MagicMock(return_value={
#         "choices": [{
#             "message": {
#                 "content": '{"header": "Generated Header", "body": "Generated Body"}'
#             }
#         }]
#     }))
#
#     handler = GetArticleHandler()
#     response = await handler(mock_app)
#
#     assert response == GetArticleResponseModel(
#         actual_date=date.today(),
#         header="Generated Header",
#         body="Generated Body"
#     )
#     mock_cache.get_cached_article.assert_called_once()
#     mock_wordsmith_client.get_awad.assert_called_once()
#     mock_openai_client.make_prompt_request.assert_called_once_with(
#         prompt=handler.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(awad="test_word")
#     )
#     mock_cache.cache_article.assert_called_once_with(
#         header="Generated Header",
#         article="Generated Body"
#     )
#
#
# async def test_get_article_json_decode_error(mock_app, mock_cache, mock_wordsmith_client, mock_openai_client):
#     mock_cache.get_cached_article.return_value = None
#     mock_wordsmith_client.get_awad.return_value = "test_word"
#     mock_openai_client.make_prompt_request.return_value = MagicMock(json=MagicMock(return_value={
#         "choices": [{
#             "message": {
#                 "content": "Invalid JSON"
#             }
#         }]
#     }))
#
#     handler = GetArticleHandler()
#     with pytest.raises(RuntimeError, match="Failed to decode JSON response"):
#         await handler(mock_app)
#
#     mock_cache.get_cached_article.assert_called_once()
#     mock_wordsmith_client.get_awad.assert_called_once()
#     mock_openai_client.make_prompt_request.assert_called_once_with(
#         prompt=handler.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(awad="test_word")
#     )
#     mock_cache.cache_article.assert_not_called()
#
#
# async def test_get_article_wordsmith_client_error(mock_app, mock_cache, mock_wordsmith_client):
#     mock_cache.get_cached_article.return_value = None
#     mock_wordsmith_client.get_awad.side_effect = RuntimeError("Wordsmith error")
#
#     handler = GetArticleHandler()
#     with pytest.raises(RuntimeError, match="Failed to fetch word of the day"):
#         await handler(mock_app)
#
#     mock_cache.get_cached_article.assert_called_once()
#     mock_wordsmith_client.get_awad.assert_called_once()
#     mock_openai_client.make_prompt_request.assert_not_called()
#     mock_cache.cache_article.assert_not_called()
#
#
# async def test_get_article_openai_client_error(mock_app, mock_cache, mock_wordsmith_client, mock_openai_client):
#     mock_cache.get_cached_article.return_value = None
#     mock_wordsmith_client.get_awad.return_value = "test_word"
#     mock_openai_client.make_prompt_request.side_effect = RuntimeError("OpenAI error")
#
#     handler = GetArticleHandler()
#     with pytest.raises(RuntimeError, match="Failed to generate article"):
#         await handler(mock_app)
#
#     mock_cache.get_cached_article.assert_called_once()
#     mock_wordsmith_client.get_awad.assert_called_once()
#     mock_openai_client.make_prompt_request.assert_called_once_with(
#         prompt=handler.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(awad="test_word")
#     )
#     mock_cache.cache_article.assert_not_called()
