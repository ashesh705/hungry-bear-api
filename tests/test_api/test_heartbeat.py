""" Test the health check routes"""

import logging

import pytest
from fastapi import status
from httpx import AsyncClient

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_heartbeat(client: AsyncClient) -> None:
    response = await client.get("/heartbeat")

    data = response.json()
    logger.debug(data)

    assert response.status_code == status.HTTP_200_OK
    assert data["status"] == "OK"
