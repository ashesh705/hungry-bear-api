""" Configuration for the API"""

import pathlib
from functools import cache
from typing import Literal

from pydantic import BaseSettings, Field

from .environment import Environment, get_environment
from .logging import configure_logging

configure_logging()


class Config(BaseSettings):
    environment: Environment

    database_uri: str


def _get_database_uri() -> str:
    directory = pathlib.Path(__file__).parent.parent.parent
    db_file = directory / "app.db"

    return f"sqlite+aiosqlite:///{db_file}"


class _DevConfig(Config):
    environment: Literal[Environment.DEVELOPMENT]

    database_uri: str = Field(default_factory=_get_database_uri)


class _ProdConfig(Config):
    environment: Literal[Environment.PRODUCTION]


class _TestConfig(Config):
    environment: Literal[Environment.TESTING]

    database_uri = "sqlite+aiosqlite:///"


@cache
def get_config() -> Config:
    env = get_environment()
    if env == Environment.DEVELOPMENT:
        return _DevConfig(environment=env)  # pragma: no cover
    elif env == Environment.PRODUCTION:
        return _ProdConfig(environment=env)  # pragma: no cover
    elif env == Environment.TESTING:
        return _TestConfig(environment=env)
    else:
        raise NotImplementedError
