import logging

import redis
from httpx import Request
from starlette.responses import JSONResponse

from api.articles.router import articles_router
import settings

from app.context import FastAPIWithContext
from api.ping.router import technical_router
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import RedisClient
from app.wordsmith import WordsmithClient
from app.openai_client import AsyncOpenAIClient

logger = logging.getLogger("app")


def include_routers():
    api_router = APIRouter(prefix="/api")
    api_router.include_router(router=articles_router)
    return api_router


def create_minimal_app() -> FastAPIWithContext:
    app = FastAPIWithContext(
        title="Articles API",
        description="Word of the Day Articles API",
        version="0.1.0",
        wordsmith_client=WordsmithClient(),
        openai_client=AsyncOpenAIClient(settings.OPENAI_API_KEY),
        redis_client=RedisClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    )

    app.include_router(router=technical_router)
    app.include_router(include_routers())

    register_errors(app)

    return app


def register_errors(app: FastAPI):
    @app.exception_handler(redis.RedisError)
    async def _(request: Request, exc: redis.RedisError):
        logger.exception("request=%s redis error: %s %s ", request, exc, getattr(exc, "info", ""))
        return JSONResponse(
            status_code=500,
            content={"detail": exc.args},
        )


def create_app() -> FastAPI:
    app = create_minimal_app()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
