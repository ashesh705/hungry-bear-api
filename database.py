""" Drop and recreate the entire database"""

import asyncio
import logging

from src.models import Base
from src.utils.database import Connection

logger = logging.getLogger(__name__)


async def main() -> None:
    conn = Connection()
    engine = conn.engine

    async with engine.begin() as db:
        logger.info("Cleaning up the database")
        await db.run_sync(Base.metadata.drop_all)

        logger.info("Recreating the database")
        await db.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())
