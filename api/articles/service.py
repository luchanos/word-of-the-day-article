import logging

from datetime import date
from api.articles.model import GetArticleResponseModel
from app.context import FastAPIWithContext
import json


logger = logging.getLogger(__name__)


class GetArticleHandler:
    GENERATE_ARTICLE_PROMPT_TEMPLATE = """
Generate an article about the word '{awad}'."
In the response I want to see json-file with two keys:
1. header - here you need to generate a header for article with max length 50 symbols.
2. body - an article about the word '{awad}' with max length 300 symbols.
"""

    async def __call__(self, app: FastAPIWithContext) -> GetArticleResponseModel:
        article = await app.redis_client.get_cached_article()
        if article is not None:
            article = json.loads(article)
            result = GetArticleResponseModel(
                actual_date=date.today(),
                header=article['header'],
                body=article['body'],
            )
        else:
            awad = await app.wordsmith_client.get_awad()
            response = await app.openai_client.make_prompt_request(
                prompt=self.GENERATE_ARTICLE_PROMPT_TEMPLATE.format(awad=awad))
            content = response.json()['choices'][0]['message']['content']
            response_data = json.loads(content)
            await app.redis_client.cache_article(header=response_data["header"], article=response_data["body"])
            result = GetArticleResponseModel(
                actual_date=date.today(),
                header=response_data['header'],
                body=response_data['body'],
            )
        return result
