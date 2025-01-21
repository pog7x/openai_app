from typing import Annotated

from fastapi import Header, HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED

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
