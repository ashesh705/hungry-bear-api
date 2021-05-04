""" Routes for getting ticker data"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.api.dependencies import get_db
from src.models import Ticker as TickerModel
from src.schemas import TickerOut

router = APIRouter()


@router.get("/", response_model=list[TickerOut])
async def get_tickers(db: AsyncSession = Depends(get_db)) -> list[TickerOut]:
    stmt = select(TickerModel).options(selectinload(TickerModel.lot_sizes))
    result = await db.execute(stmt)

    return list(map(TickerOut.from_orm, result.scalars()))


@router.get("/{symbol}", response_model=TickerOut)
async def get_ticker_by_symbol(
    symbol: str, db: AsyncSession = Depends(get_db)
) -> TickerOut:
    stmt = (
        select(TickerModel)
        .options(selectinload(TickerModel.lot_sizes))
        .filter_by(symbol=symbol)
    )
    result = await db.execute(stmt)

    ticker = result.scalars().first()
    if not ticker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticker not found"
        )

    return TickerOut.from_orm(ticker)
