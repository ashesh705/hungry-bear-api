""" Configuration for the API"""

from pydantic import BaseSettings

from .environment import Environment, get_environment
from .logging import configure_logging

configure_logging()


class Config(BaseSettings):
    environment: Environment


class _DevConfig(Config):
    pass


class _ProdConfig(Config):
    pass


class _TestConfig(Config):
    pass


def get_config() -> Config:
    env = get_environment()
    if env == Environment.DEVELOPMENT:
        return _DevConfig()
    elif env == Environment.PRODUCTION:
        return _ProdConfig()
    elif env == Environment.TESTING:
        return _TestConfig()
    else:
        raise NotImplementedError
