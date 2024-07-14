import feedparser
import httpx
from httpx import HTTPStatusError, RequestError

from app.exceptions import (
    WordsmithClientHTTPError,
    WordsmithClientParseError,
    WordsmithClientRequestError,
)


class WordsmithClient:
    def __init__(self, base_url: str = "wordsmith.org"):
        self.base_url = base_url

    async def get_awad(self) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://{self.base_url}/awad/rss1.xml")
                response.raise_for_status()
                feed = response.text
        except HTTPStatusError as e:
            raise WordsmithClientHTTPError(
                e.response.status_code, e.response.text
            ) from e
        except RequestError as e:
            raise WordsmithClientRequestError(str(e)) from e

        parsed_feed = feedparser.parse(feed)
        if not parsed_feed.entries:
            raise WordsmithClientParseError("No entries found in the RSS feed")

        word_of_the_day = parsed_feed.entries[0].title
        return word_of_the_day
