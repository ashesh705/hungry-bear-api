""" Database model for a ticker"""

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from src.schemas import MAX_LENGTH_NAME, MAX_LENGTH_SYMBOL, TickerType

from .base import Base


class Ticker(Base):
    __tablename__ = "TICKERS"

    symbol = Column("SYMBOL", String(MAX_LENGTH_SYMBOL), primary_key=True)
    name = Column("NAME", String(MAX_LENGTH_NAME), nullable=False)
    ticker_type = Column(
        "TICKER_TYPE", Enum(TickerType, create_constraint=True), nullable=False
    )

    lot_sizes = relationship(
        "LotSize", backref="ticker", cascade="all, delete-orphan"
    )


class LotSize(Base):
    __tablename__ = "LOT_SIZES"

    symbol = Column(
        "SYMBOL",
        String(MAX_LENGTH_SYMBOL),
        ForeignKey("TICKERS.SYMBOL", ondelete="CASCADE"),
        primary_key=True,
    )
    expiry = Column("EXPIRY", Date(), primary_key=True)

    lot_size = Column(
        "LOT_SIZE", Integer(), CheckConstraint("LOT_SIZE > 0"), nullable=False
    )
