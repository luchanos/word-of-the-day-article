from http import HTTPStatus
from unittest.mock import AsyncMock

from api.articles.service import GetArticleHandler
from app.cache import ArticleCache
from app.context import FastAPIWithContext
from app.openai_client import AsyncOpenAIClient
import httpx

from app.wordsmith import WordsmithClient


# cases: get article - mock WordsmithClient and OpenAI client
async def test_get_article_flow(test_cli, mocker):
    test_header = "Generated Header"
    test_body = "Test Content"
    mock_response_json = {
        "choices": [{
            "message": {
                "content": '{"header": "%s", "body": "%s"}' % (test_header, test_body)
            }
        }]
    }
    mocker.patch.object(WordsmithClient, 'get_awad', return_value='psychrophobia')
    mock_openai_response_content = httpx.Response(
        status_code=200,
        json=mock_response_json
    )
    mocker.patch.object(AsyncOpenAIClient, 'make_prompt_request', return_value=mock_openai_response_content)

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["header"] == test_header
    assert data["body"] == test_body
