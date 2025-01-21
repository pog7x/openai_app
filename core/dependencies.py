import time
from typing import Annotated

from fastapi import Header, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS

from core.config import settings


class Auth:
    def __init__(self, secret_username: str, secret_password: str):
        self._secret_username = secret_username
        self._secret_password = secret_password

    async def __call__(
        self,
        request: Request,
        username: Annotated[str | None, Header()] = None,
        password: Annotated[str | None, Header()] = None,
    ):
        if username != self._secret_username or password != self._secret_password:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


auth = Auth(settings.SECRET_USERNAME, settings.SECRET_PASSWORD)


class RateLimit:
    def __init__(self, rate_limit: int = 5, lifetime: int = 50):
        self._rate_limit: int = rate_limit
        self._lifetime: int = lifetime

    async def __call__(self, request: Request, username: Annotated[str | None, Header()] = None):
        current_time = int(time.time())

        key = f"rate_limit:{username}"

        data = await request.app.redis.get(key)

        if data:
            request_count, first_request_time = map(int, data.decode().split(":"))

            if current_time - first_request_time < self._lifetime:
                if request_count >= self._rate_limit:
                    raise HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS)
                else:
                    request_count += 1
            else:
                request_count = 1
                first_request_time = current_time
        else:
            request_count = 1
            first_request_time = current_time

        await request.app.redis.set(key, f"{request_count}:{first_request_time}", ex=self._lifetime)


rate_limit = RateLimit(rate_limit=settings.RATE_LIMIT, lifetime=settings.RATE_LIMIT_LIFETIME)
