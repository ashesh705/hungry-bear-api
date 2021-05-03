""" Pull data from NSE and update the database"""

import asyncio
import csv
import itertools
import logging
import sys
from collections.abc import Iterable
from datetime import datetime

from httpx import AsyncClient
from sqlalchemy import delete

from src.models import LotSize as LotSizeModel
from src.models import Option as OptionModel
from src.models import Ticker as TickerModel
from src.schemas import (
    LotSize,
    LotSizeData,
    Option,
    OptionType,
    Ticker,
    TickerType,
)
from src.utils.database import Connection

logger = logging.getLogger(__name__)


def _to_ticker(node: dict[str, str], ticker_type: TickerType) -> Ticker:
    DATE_FORMAT = "%b-%y"

    node = {key.strip(): value.strip() for key, value in node.items()}
    if node["SYMBOL"].upper() == "SYMBOL":
        raise ValueError("Invalid value for symbol")

    lot_sizes = []
    for key, value in node.items():
        try:
            lot_size = LotSizeData(
                date=datetime.strptime(key, DATE_FORMAT).date(), lot_size=value
            )
            lot_sizes.append(lot_size)
        except ValueError:
            continue

    return Ticker(
        symbol=node["SYMBOL"],
        name=node["UNDERLYING"],
        ticker_type=ticker_type,
        lot_size_data=lot_sizes,
    )


async def _get_tickers() -> list[Ticker]:
    url = "https://archives.nseindia.com/content/fo/fo_mktlots.csv"

    async with AsyncClient() as client:
        resp = await client.get(url)

    tickers = []
    ticker_type = TickerType.INDEX
    for row in csv.DictReader(resp.text.splitlines()):
        try:
            ticker = _to_ticker(row, ticker_type)
            tickers.append(ticker)
        except ValueError:
            ticker_type = TickerType.STOCK

    return tickers


async def _get_cookies(client: AsyncClient) -> dict:
    url = "/option-chain"

    resp = await client.get(url)
    return dict(resp.cookies)


def _get_endpoint(ticker: Ticker) -> str:
    if ticker.ticker_type == TickerType.INDEX:
        return "option-chain-indices"
    elif ticker.ticker_type == TickerType.STOCK:
        return "option-chain-equities"
    else:
        raise NotImplementedError


def _to_option_pair(node: dict) -> list[Option]:
    DATE_FORMAT = "%d-%b-%Y"
    options = []

    strike = node["strikePrice"]
    expiry = datetime.strptime(node["expiryDate"], DATE_FORMAT).date()

    ce, pe = node.get("CE"), node.get("PE")
    if ce:
        options.append(
            Option(
                symbol=ce["underlying"],
                expiry=expiry,
                option_type=OptionType.CALL,
                strike=strike,
            )
        )
    if pe:
        options.append(
            Option(
                symbol=pe["underlying"],
                expiry=expiry,
                option_type=OptionType.PUT,
                strike=strike,
            )
        )

    return options


def _to_options(node: dict) -> Iterable[Option]:
    return itertools.chain.from_iterable(map(_to_option_pair, node["data"]))


async def _get_options_for_ticker(
    ticker: Ticker, client: AsyncClient, cookies: dict
) -> Iterable[Option]:
    url = "/api/{endpoint}"
    params = {"symbol": ticker.symbol}

    resp = await client.get(
        url.format(endpoint=_get_endpoint(ticker)),
        params=params,
        cookies=cookies,
    )
    data = resp.json()

    return _to_options(data["records"])


async def _get_options(tickers: Iterable[Ticker]) -> Iterable[Option]:
    url = "https://www.nseindia.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "authority": "www.nseindia.com",
        "scheme": "https",
    }

    async with AsyncClient(
        base_url=url, headers=headers, timeout=None
    ) as client:
        cookies = await _get_cookies(client)

        tasks = map(
            lambda ticker: _get_options_for_ticker(ticker, client, cookies),
            tickers,
        )
        data = await asyncio.gather(*tasks)

    return itertools.chain.from_iterable(data)


async def _get_lot_sizes(
    tickers: Iterable[Ticker], options: list[Option]
) -> list[LotSize]:
    symbols = {o.symbol for o in options}
    expiries = {
        s: {
            o.expiry for o in filter(lambda option: option.symbol == s, options)
        }
        for s in symbols
    }

    lot_sizes = []
    for ticker in tickers:
        for expiry in expiries.get(ticker.symbol, set()):
            level = max(
                dt
                for dt in {node.date for node in ticker.lot_size_data}
                if dt <= expiry
            )
            node = next(
                node for node in ticker.lot_size_data if node.date == level
            )
            lot_size = LotSize(
                symbol=ticker.symbol, expiry=expiry, lot_size=node.lot_size
            )
            lot_sizes.append(lot_size)

    return lot_sizes


async def _save_to_database(
    tickers: Iterable[Ticker],
    lot_sizes: Iterable[LotSize],
    options: Iterable[Option],
) -> None:
    conn = Connection()

    logger.info("Opening a database session")
    session = conn.session_factory()

    try:
        logger.info("Deleting all options")
        stmt = delete(OptionModel)
        await session.execute(stmt)

        logger.info("Deleting all lot sizes")
        stmt = delete(LotSizeModel)
        await session.execute(stmt)

        logger.info("Deleting all tickers")
        stmt = delete(TickerModel)
        await session.execute(stmt)

        logger.info("Inserting new tickers")
        ticker_models = map(
            lambda t: TickerModel(**t.dict(exclude={"lot_size_data"})), tickers
        )
        session.add_all(ticker_models)

        logger.info("Inserting new lot sizes")
        lot_size_models = map(lambda l: LotSizeModel(**l.dict()), lot_sizes)
        session.add_all(lot_size_models)

        logger.info("Inserting new options")
        option_models = map(lambda o: OptionModel(**o.dict()), options)
        session.add_all(option_models)

        await session.commit()
    finally:
        logger.info("Closing the database session")
        await session.close()


async def main() -> None:
    tickers = await _get_tickers()
    tickers = list(tickers)

    options = await _get_options(tickers)
    options = list(options)

    lot_sizes = await _get_lot_sizes(tickers, options)

    await _save_to_database(tickers, lot_sizes, options)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
