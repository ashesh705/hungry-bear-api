""" Test the ticker data routes"""

import logging
from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from src.models import Ticker
from src.schemas import TickerIn, TickerType
from src.utils.database import connection

logger = logging.getLogger(__name__)


@pytest.fixture
async def ticker(api: FastAPI) -> AsyncGenerator[TickerIn, None]:
    session = connection.session_factory()
    try:
        ticker = TickerIn(
            symbol="DUMMY", name="DUMMY", ticker_type=TickerType.INDEX
        )
        model = Ticker(**ticker.dict(exclude={"lot_size_data"}))

        session.add(model)
        await session.commit()

        yield ticker
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_one_ticker(client: AsyncClient, ticker: TickerIn) -> None:
    response = await client.get(f"/ticker/{ticker.symbol}")

    data = response.json()
    logger.debug(data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_no_ticker(client: AsyncClient) -> None:
    response = await client.get("/ticker/not-exists")

    data = response.json()
    logger.debug(data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_all_tickers(client: AsyncClient, ticker: TickerIn) -> None:
    response = await client.get("/ticker")

    data = response.json()
    logger.debug(data)

    assert response.status_code == status.HTTP_200_OK
