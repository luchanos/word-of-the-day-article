from http import HTTPStatus

from app.openai_client import AsyncOpenAIClient
import httpx


async def test_get_article_from_cache(test_cli, mocker, httpx_mock):
    mock_response = """
        <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
            <channel>
                <atom:link href="https://wordsmith-test.org/awad/rss1.xml" rel="self" type="application/rss+xml"/>
                <title>Wordsmith.org: Today's Word</title>
                <link>https://wordsmith.org/</link>
                <copyright>Copyright 1994-2022 Wordsmith.org</copyright>
                <description>The magic of words - that's what Wordsmith.org is about.</description>
                <language>en-us</language>
                <ttl>1440</ttl>
                <item>
                    <title>psychrophobia</title>
                    <link>https://wordsmith.org/words/psychrophobia.html</link>
                    <description>noun: An abnormal fear of cold.</description>
                </item>
            </channel>
        </rss>
        """
    httpx_mock.add_response(url="https://wordsmith.org/awad/rss1.xml", text=mock_response)
    mock_response_json = {
        "choices": [{
            "message": {
                "content": '{"header": "Generated Header", "body": "Generated Body"}'
            }
        }]
    }
    mock_openai_response_content = httpx.Response(
        status_code=200,
        json=mock_response_json
    )
    mocker.patch.object(AsyncOpenAIClient, 'make_prompt_request', return_value=mock_openai_response_content)

    response = await test_cli.get("/api/v1/articles")
    assert response.status_code == HTTPStatus.OK
