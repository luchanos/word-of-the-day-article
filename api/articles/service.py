import logging

from datetime import date
from api.articles.model import GetArticleResponseModel
from app.context import FastAPIWithContext
import json


logger = logging.getLogger(__name__)


class GetArticleHandler:
    GENERATE_ARTICLE_PROMPT_TEMPLATE = """
Generate an article about the word '%s'."
In the response I want to see json-file with two keys:
1. header - here you need to generate a header for article with max length 50 symbols.
2. body - an article about the word '%s' with max length 300 symbols.
"""

    async def __call__(self, app: FastAPIWithContext) -> GetArticleResponseModel:
        awad = await app.wordsmith_client.get_awad()
        response = await app.openai_client.make_prompt_request(
            prompt=self.GENERATE_ARTICLE_PROMPT_TEMPLATE % (awad, ))
        content = response.json()['choices'][0]['message']['content']
        response_data = json.loads(content)
        return GetArticleResponseModel(
            actual_date=date.today(),
            header=response_data['header'],
            body=response_data['body'],
        )
