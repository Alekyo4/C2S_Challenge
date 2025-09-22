from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


class FakerProvider(Generic[TModel], ABC):
    @abstractmethod
    def create(self) -> TModel:
        raise NotImplementedError()
