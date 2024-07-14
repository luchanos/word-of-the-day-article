import logging

import redis
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import Request
from starlette.responses import JSONResponse

import settings
from api.articles.router import articles_router
from api.ping.router import technical_router
from app.context import FastAPIWithContext
from app.openai_client import AsyncOpenAIClient
from app.wordsmith import WordsmithClient

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
