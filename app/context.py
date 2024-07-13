from fastapi import FastAPI

from app.db import RedisClient
from app.openai_client import AsyncOpenAIClient
from app.wordsmith import WordsmithClient


# import aioredis


class FastAPIWithContext(FastAPI):
    wordsmith_client: WordsmithClient
    openai_client: AsyncOpenAIClient
    redis_client: RedisClient

    def __init__(
            self, *args,
            wordsmith_client: WordsmithClient,
            openai_client: AsyncOpenAIClient,
            redis_client: RedisClient,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.wordsmith_client = wordsmith_client
        self.openai_client = openai_client
        self.redis_client = redis_client
