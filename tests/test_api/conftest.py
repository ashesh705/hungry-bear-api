""" Fixtures for testing the API"""

from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from src.api import API, create_api


@pytest.fixture
def api() -> Generator[API, None, None]:
    yield create_api()


@pytest.fixture
async def client(api: API) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=api, base_url="http://test") as client:
        yield client
