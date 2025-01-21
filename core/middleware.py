import logging
import time

from aioredis import Redis
from fastapi import Request, Response
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthMiddleware:
    def __init__(self, secret_username: str, secret_password: str):
        self._secret_username = secret_username
        self._secret_password = secret_password

    async def __call__(self, request: Request, call_next):
        username = request.headers.get("username")
        password = request.headers.get("password")

        if username != self._secret_username or password != self._secret_password:
            return JSONResponse(None, status_code=HTTP_401_UNAUTHORIZED)

        return await call_next(request)


class RateLimitMiddleware:
    def __init__(self, redis_cli: Redis, rate_limit: int = 5, lifetime: int = 50):
        self._redis_cli: Redis = redis_cli
        self._rate_limit: int = rate_limit
        self._lifetime: int = lifetime

    async def __call__(self, request: Request, call_next):
        current_time = int(time.time())
        username = request.headers.get("username")

        key = f"rate_limit:{username}"

        data = await self._redis_cli.get(key)

        if data:
            request_count, first_request_time = map(int, data.decode().split(":"))

            if current_time - first_request_time < self._lifetime:
                if request_count >= self._rate_limit:
                    return JSONResponse(None, status_code=HTTP_429_TOO_MANY_REQUESTS)
                else:
                    request_count += 1
            else:
                request_count = 1
                first_request_time = current_time
        else:
            request_count = 1
            first_request_time = current_time

        await self._redis_cli.set(key, f"{request_count}:{first_request_time}", ex=self._lifetime)

        return await call_next(request)


class LoggingMiddleware:

    async def __call__(self, request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")

        response: Response = await call_next(request)

        logger.info(f"Outgoing response: {response.status_code} {request.url}")

        return response
