from http import HTTPStatus

import httpx

from api.articles.service import GetArticleHandler


async def test_get_article_flow(test_cli, mocker, test_app):
    """Generate an article for the first time: make requests to all clients + save an article to the cache."""
    assert not test_app.cache["article"].cache
    test_header = "Generated Header"
    test_body = "Test Content"
    mock_response_json = {
        "choices": [
            {
                "message": {
                    "content": '{"header": "%s", "body": "%s"}'
                    % (test_header, test_body)
                }
            }
        ]
    }
    mock_cache = mocker.patch(
        'app.cache.ArticleCache.get_cached_article', return_value=None
    )
    mock_cache_article = mocker.patch(
        'app.cache.ArticleCache.cache_article', return_value=None
    )
    mock_get_awad = mocker.patch.object(
        test_app.wordsmith_client, 'get_awad', return_value='psychrophobia'
    )
    mock_openai_response_content = httpx.Response(
        status_code=200, json=mock_response_json
    )

    async def mock_make_prompt_request(*args, **kwargs):
        return mock_openai_response_content

    mock_make_prompt_request = mocker.patch.object(
        test_app.openai_client,
        'make_prompt_request',
        side_effect=mock_make_prompt_request,
    )

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["header"] == test_header
    assert data["body"] == test_body

    mock_cache.assert_called_once()
    mock_cache_article.assert_called_once_with(header=test_header, article=test_body)

    mock_get_awad.assert_called_once()
    mock_make_prompt_request.assert_called_once_with(
        prompt=GetArticleHandler.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(
            awad="psychrophobia"
        )
    )


async def test_get_article_from_cache(test_cli, mocker, test_app):
    """Retrieve an article from the cache: no external client requests."""
    test_header = "Cached Header"
    test_body = "Cached Content"
    mock_cache = mocker.patch(
        'app.cache.ArticleCache.get_cached_article',
        return_value={"header": test_header, "body": test_body},
    )

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["header"] == test_header
    assert data["body"] == test_body

    mock_cache.assert_called_once()
    test_app.wordsmith_client.get_awad.assert_not_called()
    test_app.openai_client.make_prompt_request.assert_not_called()


async def test_get_article_json_decode_error(test_cli, mocker, test_app):
    """Handle JSON decode error from OpenAI client."""
    mock_cache = mocker.patch(
        'app.cache.ArticleCache.get_cached_article', return_value=None
    )
    mock_cache_article = mocker.patch(
        'app.cache.ArticleCache.cache_article', return_value=None
    )
    mock_get_awad = mocker.patch.object(
        test_app.wordsmith_client, 'get_awad', return_value='psychrophobia'
    )

    mock_openai_response_content = httpx.Response(
        status_code=200,
        content=b'Invalid JSON',
        headers={"Content-Type": "application/json"},
    )

    async def mock_make_prompt_request(*args, **kwargs):
        return mock_openai_response_content

    mock_make_prompt_request = mocker.patch.object(
        test_app.openai_client,
        'make_prompt_request',
        side_effect=mock_make_prompt_request,
    )

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Internal server error"

    mock_cache.assert_called_once()
    mock_cache_article.assert_not_called()
    mock_get_awad.assert_called_once()
    mock_make_prompt_request.assert_called_once_with(
        prompt=GetArticleHandler.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(
            awad="psychrophobia"
        )
    )


async def test_get_article_wordsmith_client_error(test_cli, mocker, test_app):
    """Handle error from Wordsmith client."""
    mock_cache = mocker.patch(
        'app.cache.ArticleCache.get_cached_article', return_value=None
    )
    mock_cache_article = mocker.patch(
        'app.cache.ArticleCache.cache_article', return_value=None
    )

    mock_get_awad = mocker.patch.object(
        test_app.wordsmith_client,
        'get_awad',
        side_effect=RuntimeError("Wordsmith error"),
    )

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Internal server error"

    mock_cache.assert_called_once()
    mock_cache_article.assert_not_called()
    mock_get_awad.assert_called_once()
    test_app.openai_client.make_prompt_request.assert_not_called()


async def test_get_article_openai_client_error(test_cli, mocker, test_app):
    """Handle error from OpenAI client."""
    mock_cache = mocker.patch(
        'app.cache.ArticleCache.get_cached_article', return_value=None
    )
    mock_cache_article = mocker.patch(
        'app.cache.ArticleCache.cache_article', return_value=None
    )

    mock_get_awad = mocker.patch.object(
        test_app.wordsmith_client, 'get_awad', return_value='psychrophobia'
    )
    mock_make_prompt_request = mocker.patch.object(
        test_app.openai_client,
        'make_prompt_request',
        side_effect=RuntimeError("OpenAI error"),
    )

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["detail"] == "Internal server error"

    mock_cache.assert_called_once()
    mock_cache_article.assert_not_called()
    mock_get_awad.assert_called_once()
    mock_make_prompt_request.assert_called_once_with(
        prompt=GetArticleHandler.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(
            awad="psychrophobia"
        )
    )
