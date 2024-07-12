import logging

from datetime import date
from api.articles.model import GetArticleResponseModel
from app.context import FastAPIWithContext


logger = logging.getLogger(__name__)


class GetArticleHandler:
    async def __call__(self, app: FastAPIWithContext) -> GetArticleResponseModel:
        awad = await app.wordsmith_client.get_awad()
        return GetArticleResponseModel(
            actual_date=date.today(),
            header=f"TEST HEADER about {awad}",
            content="TEST CONTENT",
        )
