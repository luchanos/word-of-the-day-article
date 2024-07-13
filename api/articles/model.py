from pydantic import BaseModel, Field
from datetime import date


class GetArticleResponseModel(BaseModel):
    header: str = Field(..., description="The header of the article")
    body: str = Field(..., description="The body content of the article, up to 300 characters")
