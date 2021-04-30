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


class LotSize(Base):
    expiry: date
    lot_size: int = Field(gt=0)


class Ticker(Base):
    symbol: str = Field(min_length=1, max_length=MAX_LENGTH_SYMBOL)
    name: str = Field(min_length=1, max_length=MAX_LENGTH_NAME)
    underlying_type: TickerType

    lot_sizes: list[LotSize]
