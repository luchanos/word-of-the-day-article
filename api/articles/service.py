import logging

from datetime import date
from api.articles.model import GetArticleResponseModel
from app.context import FastAPIWithContext


logger = logging.getLogger(__name__)


class GetArticleHandler:
    async def __call__(self, app: FastAPIWithContext) -> GetArticleResponseModel:
        return GetArticleResponseModel(
            actual_date=date.today(),
            header="TEST HEADER",
            content="TEST CONTENT",
        )
