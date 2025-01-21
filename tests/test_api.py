import pytest
from httpx import AsyncClient, codes

from core.config import settings


class TestAPI:
    @pytest.mark.asyncio
    async def test_unauthorized(self, http_client: AsyncClient):
        resp = await http_client.get("/processed-texts")
        assert resp.is_error
        assert resp.status_code == codes.UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_rate_limit(self, http_client: AsyncClient):
        for _ in range(settings.RATE_LIMIT + 1):
            resp = await http_client.get(
                "/processed-texts",
                headers={"username": settings.SECRET_USERNAME, "password": settings.SECRET_PASSWORD},
            )
        assert resp.is_error
        assert resp.status_code == codes.TOO_MANY_REQUESTS
