from fastapi import FastAPI

from app.wordsmith import WordsmithClient


# import aioredis


class FastAPIWithContext(FastAPI):
    wordsmith_client: WordsmithClient
    # redis_pool: aioredis.ConnectionPool

    def __init__(self, *args, wordsmith_client: WordsmithClient, **kwargs):
        super().__init__(*args, **kwargs)
        self.wordsmith_client = wordsmith_client
