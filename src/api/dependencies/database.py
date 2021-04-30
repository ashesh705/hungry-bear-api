""" Inject database session in API routes"""

import logging
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import Connection

logger = logging.getLogger(__name__)


async def get_db(
    conn: Connection = Depends(),
) -> AsyncGenerator[AsyncSession, None]:
    logger.debug("Opening a database session")
    session = conn.session_factory()

    try:
        yield session
    finally:
        logger.debug("Closing the database session")
        session.close()
