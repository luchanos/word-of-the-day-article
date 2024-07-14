import httpx
import pytest

import settings
from app.openai_client import AsyncOpenAIClient


@pytest.mark.asyncio
async def test_make_prompt_request_success(httpx_mock):
    mock_response = {
        "choices": [
            {"message": {"content": '{"header": "Test Header", "body": "Test Body"}'}}
        ]
    }
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
        json=mock_response,
    )

    client = AsyncOpenAIClient(api_key=settings.OPENAI_TEST_API_KEY)
    response = await client.make_prompt_request(prompt="Hello!")
    response_data = response.json()

    assert response.status_code == 200
    assert (
        response_data["choices"][0]["message"]["content"]
        == '{"header": "Test Header", "body": "Test Body"}'
    )


@pytest.mark.asyncio
async def test_make_prompt_request_http_error(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
        status_code=404,
        json={"error": "Not Found"},
    )

    client = AsyncOpenAIClient(api_key=settings.OPENAI_TEST_API_KEY)
    with pytest.raises(RuntimeError, match="HTTP error occurred"):
        await client.make_prompt_request(prompt="Hello!")


@pytest.mark.asyncio
async def test_make_prompt_request_request_error(httpx_mock):
    exception = httpx.ConnectError("Connection error")
    httpx_mock.add_exception(
        exception, url="https://api.openai.com/v1/chat/completions"
    )

    client = AsyncOpenAIClient(api_key=settings.OPENAI_TEST_API_KEY)
    with pytest.raises(RuntimeError, match="Request error occurred"):
        await client.make_prompt_request(prompt="Hello!")
