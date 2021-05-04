""" Utilities for database connections"""

from functools import cached_property
from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.config import get_config


class _Connection:
    @cached_property
    def _database_uri(self) -> str:
        config = get_config()
        return config.database_uri

    @cached_property
    def _connect_args(self) -> Optional[dict[str, bool]]:
        if self._database_uri.startswith("sqlite"):
            return {"check_same_thread": False}

        return None

    @cached_property
    def engine(self) -> AsyncEngine:
        kwargs = (
            {"connect_args": self._connect_args} if self._connect_args else {}
        )

        return create_async_engine(
            self._database_uri, pool_pre_ping=True, **kwargs, future=True
        )

    @cached_property
    def session_factory(self) -> sessionmaker:
        return sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
            future=True,
        )


connection = _Connection()
