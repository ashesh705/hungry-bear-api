""" Basic schema to use"""

from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class Base(BaseModel):
    class Config:
        validate_assignment = True
        orm_mode = True


_T = TypeVar("_T")


class ToList(Base, GenericModel, Generic[_T]):
    __root__: list[_T]

    def to_list(self) -> list[_T]:
        return self.__root__
