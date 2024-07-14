import httpx
import pytest

from app.exceptions import (
    WordsmithClientHTTPError,
    WordsmithClientParseError,
    WordsmithClientRequestError,
)
from app.wordsmith import WordsmithClient


async def test_get_awad_success(httpx_mock):
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
    httpx_mock.add_response(
        url="https://wordsmith-test.org/awad/rss1.xml", text=mock_response
    )

    client = WordsmithClient(base_url="wordsmith-test.org")
    word = await client.get_awad()
    assert word == "psychrophobia"


async def test_get_awad_http_error(httpx_mock):
    httpx_mock.add_response(
        url="https://wordsmith-test.org/awad/rss1.xml", status_code=404
    )

    client = WordsmithClient(base_url="wordsmith-test.org")
    with pytest.raises(WordsmithClientHTTPError, match="HTTP error occurred: 404"):
        await client.get_awad()


async def test_get_awad_request_error(httpx_mock):
    exception = httpx.ConnectError("Connection error")
    httpx_mock.add_exception(exception, url="https://wordsmith-test.org/awad/rss1.xml")

    client = WordsmithClient(base_url="wordsmith-test.org")
    with pytest.raises(WordsmithClientRequestError, match="Connection error"):
        await client.get_awad()


async def test_get_awad_no_entries(httpx_mock):
    mock_response = """
    <rss>
        <channel>
        </channel>
    </rss>
    """
    httpx_mock.add_response(
        url="https://wordsmith-test.org/awad/rss1.xml", text=mock_response
    )

    client = WordsmithClient(base_url="wordsmith-test.org")
    with pytest.raises(
        WordsmithClientParseError, match="No entries found in the RSS feed"
    ):
        await client.get_awad()
