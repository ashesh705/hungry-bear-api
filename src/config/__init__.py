""" Configuration for the API"""

import abc
import json
import pathlib
from functools import cache
from typing import Literal

from pydantic import BaseSettings

from .environment import Environment, get_environment
from .logging import configure_logging

configure_logging()


class Config(BaseSettings, abc.ABC):
    environment: Environment

    @property
    @abc.abstractmethod
    def database_uri(self) -> str:
        raise NotImplementedError


class _DevConfig(Config):
    environment: Literal[Environment.DEVELOPMENT]

    @property
    def database_uri(self) -> str:  # pragma: no cover
        directory = pathlib.Path(__file__).parent.parent.parent
        db_file = directory / "app.db"

        return f"sqlite+aiosqlite:///{db_file}"


class DatabaseConfig(BaseSettings):
    host: str
    port: int

    database: str

    user: str
    password: str


class _ProdConfig(Config):
    environment: Literal[Environment.PRODUCTION]

    @property
    def database_uri(self) -> str:  # pragma: no cover
        directory = pathlib.Path(__file__).parent.parent.parent
        config_file = directory / "database.json"

        with config_file.open() as f:
            ob = DatabaseConfig.parse_obj(json.load(f))

        return (
            f"postgresql+asyncpg://{ob.user}:{ob.password}"
            f"@{ob.host}:{ob.port}/{ob.database}"
        )


class _TestConfig(Config):
    environment: Literal[Environment.TESTING]

    @property
    def database_uri(self) -> str:
        return "sqlite+aiosqlite:///"


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
