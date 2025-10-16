from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

from c2s_challenge.server.database.provider import DatabaseProvider

TModel = TypeVar("TModel", bound=BaseModel)


class SeederProvider(Generic[TModel], ABC):
    def __init__(self, database: DatabaseProvider):
        raise NotImplementedError()

    @abstractmethod
    def run(self, num: int) -> None:
        raise NotImplementedError()
