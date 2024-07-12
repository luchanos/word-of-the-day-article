from http import HTTPStatus

from fastapi import APIRouter, Depends
from starlette.requests import Request

from api.articles.model import GetArticleResponseModel
from api.articles.service import GetArticleHandler

articles_router = APIRouter(tags=["articles"])


@articles_router.get(
    path="/v1/articles",
    status_code=HTTPStatus.OK,
    description="Get an Article of the Day from cache or Create a New One",
    summary="Get an Article of the Day",
    response_model=GetArticleResponseModel,
)
async def get_article(request: Request, handler=Depends(GetArticleHandler)):
    return await handler(request.app)
