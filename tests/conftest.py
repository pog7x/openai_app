import asyncio
from typing import Any, AsyncIterator, Awaitable

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

TestApp = Awaitable[dict[str, Any]], (dict[str, Any])


@pytest.fixture(scope="session")
def application() -> TestApp:
    from core.app import app_factory

    return app_factory()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def redis_flushall(application: TestApp):
    yield
    await application.redis.execute_command("FLUSHALL")


@pytest_asyncio.fixture(scope="session")
async def http_client(application: TestApp) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=application),
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
