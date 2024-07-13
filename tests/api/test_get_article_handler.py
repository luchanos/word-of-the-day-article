from http import HTTPStatus

from api.articles.service import GetArticleHandler
import httpx


# cases: get article - mock WordsmithClient and OpenAI client
async def test_get_article_flow(test_cli, mocker, test_app):
    """Generate an article for the first time: make requests to all clients + save an article to the cache."""
    test_header = "Generated Header"
    test_body = "Test Content"
    mock_response_json = {
        "choices": [{
            "message": {
                "content": '{"header": "%s", "body": "%s"}' % (test_header, test_body)
            }
        }]
    }
    mock_cache = mocker.patch('app.cache.ArticleCache.get_cached_article', return_value=None)
    mock_cache_article = mocker.patch('app.cache.ArticleCache.cache_article', return_value=None)
    mock_get_awad = mocker.patch.object(test_app.wordsmith_client, 'get_awad', return_value='psychrophobia')
    mock_openai_response_content = httpx.Response(
        status_code=200,
        json=mock_response_json
    )

    async def mock_make_prompt_request(*args, **kwargs):
        return mock_openai_response_content

    mock_make_prompt_request = mocker.patch.object(test_app.openai_client, 'make_prompt_request', side_effect=mock_make_prompt_request)

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["header"] == test_header
    assert data["body"] == test_body

    mock_cache.assert_called_once()
    mock_cache_article.assert_called_once_with(
        header=test_header,
        article=test_body
    )

    mock_get_awad.assert_called_once()
    mock_make_prompt_request.assert_called_once_with(
        prompt=GetArticleHandler.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(awad="psychrophobia")
    )
