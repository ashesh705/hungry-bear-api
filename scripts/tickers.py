""" Get ticker data from NSE and update the database"""

import asyncio
import csv
import logging
import sys

import httpx
from sqlalchemy import delete

from src.models import Ticker as TickerModel
from src.schemas import Ticker, TickerType
from src.utils.database import Connection

logger = logging.getLogger(__name__)

_url = "https://archives.nseindia.com/content/fo/fo_mktlots.csv"


def _get_ticker(node: dict[str, str], ticker_type: TickerType) -> Ticker:
    node = {key.strip(): value.strip() for key, value in node.items()}
    if node["SYMBOL"].upper() == "SYMBOL":
        raise ValueError("Invalid value for symbol")

    return Ticker(
        symbol=node["SYMBOL"], name=node["UNDERLYING"], ticker_type=ticker_type
    )


async def main() -> None:
    async with httpx.AsyncClient() as client:
        resp = await client.get(_url)

    tickers = []
    ticker_type = TickerType.INDEX
    for row in csv.DictReader(resp.text.splitlines()):
        try:
            ticker = _get_ticker(row, ticker_type)
            tickers.append(ticker)
        except ValueError:
            ticker_type = TickerType.STOCK

    conn = Connection()

    logger.info("Opening a database session")
    session = conn.session_factory()

    try:
        logger.debug("Deleting all tickers")
        stmt = delete(TickerModel)
        await session.execute(stmt)

        logger.debug("Inserting new tickers")
        models = map(lambda t: TickerModel(**t.dict()), tickers)
        session.add_all(models)

        await session.commit()
    finally:
        logger.info("Closing the database session")
        await session.close()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
