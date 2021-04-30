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
    __tablename__ = "OPTIONS"

    symbol = Column(
        "SYMBOL",
        String(MAX_LENGTH_SYMBOL),
        ForeignKey("TICKERS.SYMBOL", ondelete="CASCADE"),
        primary_key=True,
    )
    expiry = Column("EXPIRY", Date(), primary_key=True)

    option_type = Column(
        "OPTION_TYPE",
        Enum(OptionType, create_constraint=True),
        primary_key=True,
    )
    strike = Column(
        "STRIKE", Numeric(), CheckConstraint("STRIKE > 0"), primary_key=True
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ("SYMBOL", "EXPIRY"),
            ["LOT_SIZES.SYMBOL", "LOT_SIZES.EXPIRY"],
            ondelete="CASCADE",
        ),
    )
