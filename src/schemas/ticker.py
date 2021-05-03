""" Schema for a ticker"""

from datetime import date
from enum import Enum

from pydantic import Field

from .base import Base

MAX_LENGTH_SYMBOL = 100
MAX_LENGTH_NAME = 1000


class TickerType(Enum):
    STOCK = "STOCK"
    INDEX = "INDEX"


class LotSizeData(Base):
    date: date
    lot_size: int


class Ticker(Base):
    symbol: str = Field(min_length=1, max_length=MAX_LENGTH_SYMBOL)
    name: str = Field(min_length=1, max_length=MAX_LENGTH_NAME)
    ticker_type: TickerType

    lot_size_data: list[LotSizeData] = []


class LotSize(Base):
    symbol: str = Field(min_length=1, max_length=MAX_LENGTH_SYMBOL)
    expiry: date
    lot_size: int = Field(gt=0)
