""" List all enabled routers"""

from fastapi import APIRouter
from pydantic import BaseModel, validator

from .heartbeat import router as heartbeat_router
from .ticker import router as ticker_router


class _Router(BaseModel):
    prefix: str
    api_router: APIRouter

    @validator("prefix")
    def is_valid_prefix(cls, v: str) -> str:
        if not v.startswith("/"):  # pragma: no cover
            raise ValueError(f"Invalid prefix {v}, must start with /")

        return v

    @property
    def name(self) -> str:
        return self.api_router.__class__.__name__

    class Config:
        arbitrary_types_allowed = True


routers = [
    _Router(prefix="/heartbeat", api_router=heartbeat_router),
    _Router(prefix="/ticker", api_router=ticker_router),
]
