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
    __tablename__ = "tickers"

    symbol = Column(String(MAX_LENGTH_SYMBOL), primary_key=True)
    name = Column(String(MAX_LENGTH_NAME), nullable=False)
    ticker_type = Column(
        Enum(TickerType, create_constraint=True), nullable=False
    )

    lot_sizes = relationship(
        "LotSize", backref="ticker", cascade="all, delete-orphan"
    )


class LotSize(Base):
    __tablename__ = "lot_sizes"

    symbol = Column(
        String(MAX_LENGTH_SYMBOL),
        ForeignKey("tickers.symbol", ondelete="CASCADE"),
        primary_key=True,
    )
    expiry = Column("expiry", Date(), primary_key=True)

    lot_size = Column(
        "lot_size", Integer(), CheckConstraint("lot_size > 0"), nullable=False
    )
