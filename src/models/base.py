""" Base class for database models"""

from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    """Base class for SQL Alchemy models"""

    metadata: MetaData

    def __init__(self, **kwargs: Any) -> None:
        for field, value in kwargs.items():
            setattr(self, field, value)
