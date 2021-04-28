""" Different operating environments for the API"""

from enum import Enum

from pydantic import BaseSettings


class Environment(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"
    TESTING = "TESTING"


class _EnvConfig(BaseSettings):
    environment: Environment

    class Config:
        env_file = ".env"


def get_environment() -> Environment:
    return _EnvConfig().environment
