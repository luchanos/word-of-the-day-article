import logging
from contextlib import asynccontextmanager
from api.articles.router import articles_router
import settings

from app.context import FastAPIWithContext
from api.ping.router import technical_router
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.wordsmith import WordsmithClient
from app.openai_client import AsyncOpenAIClient

logger = logging.getLogger("app")


def include_routers():
    api_router = APIRouter(prefix="/api")
    api_router.include_router(router=articles_router)
    return api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # app.redis_pool = await RedisClient.setup_redis_db_pool()
    yield
    # await app.redis_db_pool.close()


def create_minimal_app() -> FastAPIWithContext:
    app = FastAPIWithContext(
        title="Articles API",
        description="Word of the Day Articles API",
        version="0.1.0",
        lifespan=lifespan,
        wordsmith_client=WordsmithClient(),
        openai_client=AsyncOpenAIClient(settings.OPENAI_API_KEY),
    )

    app.include_router(router=technical_router)
    app.include_router(include_routers())

    # register_errors(app)

    return app


# todo luchanos make for redis
# def register_errors(app: FastAPI):
#     @app.exception_handler(opensearchpy.OpenSearchException)
#     async def _(request: Request, exc: opensearchpy.OpenSearchException):
#         logger.exception("request=%s opensearch error: %s %s ", request, exc, getattr(exc, "info", ""))
#         return JSONResponse(
#             status_code=500,
#             content={"detail": exc.args},
#         )


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
