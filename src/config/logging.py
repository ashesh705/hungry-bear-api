""" Configure logging for the application"""

import pathlib
from logging.config import fileConfig


def configure_logging() -> None:
    file = pathlib.Path(__file__).parent / "store" / "logging.ini"
    fileConfig(file, disable_existing_loggers=False)
