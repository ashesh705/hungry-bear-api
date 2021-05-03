""" Fixtures for testing the API"""

import logging
from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.api import create_api
from src.models import Base
from src.utils.database import connection

logger = logging.getLogger(__name__)


@pytest.fixture
async def api() -> AsyncGenerator[FastAPI, None]:
    engine = connection.engine

    async with engine.begin() as db:
        logger.info("Creating all tables")
        await db.run_sync(Base.metadata.create_all)

        yield create_api()

        logger.info("Dropping all tables")
        await db.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(api: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=api, base_url="http://test") as client:
        yield client
