import httpx
import feedparser


class WordsmithClient:
    def __init__(self, base_url: str = "wordsmith.org"):
        self.base_url = base_url

    async def get_awad(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://{self.base_url}/awad/rss1.xml")
            response.raise_for_status()
            feed = response.text
        parsed_feed = feedparser.parse(feed)
        word_of_the_day = parsed_feed.entries[0].title
        return word_of_the_day
