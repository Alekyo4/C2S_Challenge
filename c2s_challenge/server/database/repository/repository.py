from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel
from sqlalchemy import BinaryExpression, Column, Select, String, cast, select
from sqlalchemy.orm import Session

from ..orm import BaseORM


class DatabaseRepository(ABC):
    def __init__(self, session: Session):
        raise NotImplementedError()

    @abstractmethod
    def add(self, entity: BaseModel) -> BaseModel:
        raise NotImplementedError()

    @abstractmethod
    def search(
        self, filter: BaseModel, offset: int = 0, limit: int = 0
    ) -> tuple[list[BaseORM], int]:
        raise NotImplementedError()

    def _make_select_filter(
        self, orm: BaseORM, ex_filter: BaseModel | dict[str, any]
    ) -> Select:
        query: Select[any] = select(orm)

        filter: dict[str, any] = (
            ex_filter.model_dump() if isinstance(ex_filter, BaseModel) else ex_filter
        )

        for field, value in filter.items():
            if value is None:
                continue

            column: Column | None = getattr(orm, field) if hasattr(orm, field) else None

            if isinstance(value, str) and column:
                query = query.where(column.ilike(f"%{value}%"))
            elif isinstance(value, Enum) and column:
                column_cast: BinaryExpression[bool] = cast(column, String).ilike(
                    other=f"%{value.value}%"
                )

                query = query.where(column_cast)
            elif isinstance(value, ((Decimal, float, int))):
                if column is not None:
                    query = query.where(column == value)
                    continue

                num_column: Column = getattr(orm, field.split("_", 1).pop())

                if field.startswith("min_"):
                    query = query.where(num_column >= value)
                elif field.startswith("max_"):
                    query = query.where(num_column <= value)
            else:
                raise TypeError(
                    f"The '{field}' field of the passed filter cannot be parsed"
                )

        return query
