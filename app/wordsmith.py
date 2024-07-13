import httpx
import feedparser
from httpx import HTTPStatusError, RequestError


class WordsmithClient:
    def __init__(self, base_url: str = "wordsmith.org"):
        self.base_url = base_url

    async def get_awad(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://{self.base_url}/awad/rss1.xml")
                response.raise_for_status()
                feed = response.text
        except (HTTPStatusError, RequestError) as e:
            raise RuntimeError(f"Error fetching word of the day: {str(e)}")

        parsed_feed = feedparser.parse(feed)
        if not parsed_feed.entries:
            raise RuntimeError("No entries found in the RSS feed")

        word_of_the_day = parsed_feed.entries[0].title
        return word_of_the_day
