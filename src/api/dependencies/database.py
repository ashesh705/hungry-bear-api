""" Inject database session in API routes"""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import connection

logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    logger.debug("Opening a database session")
    session = connection.session_factory()

    try:
        yield session
    finally:
        logger.debug("Closing the database session")
        await session.close()
