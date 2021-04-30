""" Schema for an option"""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import Field

from .base import Base
from .ticker import MAX_LENGTH_SYMBOL


class OptionType(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


class Option(Base):
    symbol: str = Field(min_length=1, max_length=MAX_LENGTH_SYMBOL)
    expiry: date

    option_type: OptionType
    strike: Decimal = Field(gt=0)
