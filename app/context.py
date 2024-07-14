from fastapi import FastAPI

from app.cache import ArticleCache
from app.openai_client import AsyncOpenAIClient
from app.wordsmith import WordsmithClient


class FastAPIWithContext(FastAPI):
    def __init__(
        self,
        *args,
        wordsmith_client: WordsmithClient,
        openai_client: AsyncOpenAIClient,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.wordsmith_client = wordsmith_client
        self.openai_client = openai_client
        self.cache = {"article": ArticleCache()}
