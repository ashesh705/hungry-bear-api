""" Database model for an option"""

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    Numeric,
    String,
)

from src.schemas import MAX_LENGTH_SYMBOL, OptionType

from .base import Base


class Option(Base):
    __tablename__ = "options"

    symbol = Column(
        String(MAX_LENGTH_SYMBOL),
        ForeignKey("tickers.symbol", ondelete="CASCADE"),
        primary_key=True,
    )
    expiry = Column(Date(), primary_key=True)

    option_type = Column(
        Enum(OptionType, create_constraint=True),
        primary_key=True,
    )
    strike = Column(Numeric(), CheckConstraint("strike > 0"), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ("symbol", "expiry"),
            ["lot_sizes.symbol", "lot_sizes.expiry"],
            ondelete="CASCADE",
        ),
    )
