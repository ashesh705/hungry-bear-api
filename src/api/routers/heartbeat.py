""" Routes for checking health of API"""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class _HeartBeat(BaseModel):
    status: Literal["OK"] = "OK"


@router.get("/", response_model=_HeartBeat)
async def get_heartbeat() -> _HeartBeat:
    return _HeartBeat()
