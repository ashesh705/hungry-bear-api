""" Global fixtures for the project"""

import pytest
from pytest import MonkeyPatch

from src.config import Environment


@pytest.fixture(autouse=True)
def set_environment(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", Environment.TESTING.value)
