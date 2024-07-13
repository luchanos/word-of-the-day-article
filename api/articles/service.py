import logging
from datetime import date
import json

from fastapi import HTTPException

from api.articles.model import GetArticleResponseModel
from app.context import FastAPIWithContext

logger = logging.getLogger(__name__)


class GetArticleHandler:
    GENERATE_ARTICLE_PROMPT_TEMPLATE = """
Generate an article about the word '{awad}'.
In the response I want to see 100% valid for json.loads() json-file with two keys:
1. header - here you need to generate a header for article with max length 50 symbols.
2. body - an article about the word '{awad}' with max length 300 symbols.
"""

    async def __call__(self, app: FastAPIWithContext) -> GetArticleResponseModel:
        try:
            article = await app.cache["article"].get_cached_article()
            if article:
                logger.info("Cache hit: Retrieved article from cache")
                return self.build_response(article)

            awad = await self.get_word_of_the_day(app)
            response_data = await self.generate_article(app, awad)

            await app.cache["article"].cache_article(
                header=response_data["header"],
                article=response_data["body"]
            )

            return self.build_response(response_data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to decode JSON response")
        except Exception as e:
            logger.error(f"Failed to get article: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get article")

    @staticmethod
    def build_response(data: dict) -> GetArticleResponseModel:
        return GetArticleResponseModel(
            actual_date=date.today(),
            header=data['header'],
            body=data['body'],
        )

    @staticmethod
    async def get_word_of_the_day(app: FastAPIWithContext) -> str:
        try:
            return await app.wordsmith_client.get_awad()
        except Exception as e:
            logger.error(f"Failed to fetch word of the day: {str(e)}")
            raise RuntimeError("Failed to fetch word of the day") from e

    async def generate_article(self, app: FastAPIWithContext, awad: str) -> dict:
        try:
            response = await app.openai_client.make_prompt_request(
                prompt=self.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(awad=awad)
            )
            content = response.json()['choices'][0]['message']['content']
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to generate article: {str(e)}")
            raise RuntimeError("Failed to generate article") from e
