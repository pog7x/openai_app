import aioredis
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from api.routes import router
from clients.openai_client import OpenAICLient
from core.config import settings
from core.middleware import LoggingMiddleware
from repositories.repository import ProcessedTextRepo
from services.service import ProcessedTextService


class ApplicationFactory:
    def __call__(self) -> ASGIApp:
        application = FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.PROJECT_VERSION,
            debug=settings.DEBUG,
            root_path=settings.ROOT_URL,
            openapi_url=settings.OPENAPI_URL,
            docs_url=None if settings.DISABLE_DOCS else settings.DOCS_URL,
        )
        application.include_router(router)
        self._add_dependencies(app=application)
        self._init_middlewares(app=application)
        return application

    @staticmethod
    def _add_dependencies(app: FastAPI) -> None:
        app.redis = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        )
        app.openai = OpenAICLient(api_key=settings.OPENAI_API_KEY)
        app.repo = ProcessedTextRepo(redis_cli=app.redis)
        app.service = ProcessedTextService(repo=app.repo, openai=app.openai)

    @staticmethod
    def _init_middlewares(app: FastAPI) -> None:
        # Logging
        app.add_middleware(BaseHTTPMiddleware, LoggingMiddleware())


app_factory = ApplicationFactory()
