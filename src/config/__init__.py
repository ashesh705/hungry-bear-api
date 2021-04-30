""" Configuration for the API"""

import json
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


def _get_dev_database_uri() -> str:
    directory = pathlib.Path(__file__).parent.parent.parent
    db_file = directory / "app.db"

    return f"sqlite+aiosqlite:///{db_file}"


class DatabaseConfig(BaseSettings):
    host: str
    port: int

    database: str

    user: str
    password: str


def _get_prod_database_uri() -> str:
    directory = pathlib.Path(__file__).parent.parent.parent
    config_file = directory / "database.json"

    with config_file.open() as f:
        ob = DatabaseConfig.parse_obj(json.load(f))

    return (
        f"postgresql+asyncpg://{ob.user}:{ob.password}"
        f"@{ob.host}:{ob.port}/{ob.database}"
    )


class _DevConfig(Config):
    environment: Literal[Environment.DEVELOPMENT]

    database_uri: str = Field(default_factory=_get_dev_database_uri)


class _ProdConfig(Config):
    environment: Literal[Environment.PRODUCTION]

    database_uri: str = Field(default_factory=_get_prod_database_uri)


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
