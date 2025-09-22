from sqlalchemy import Select, Sequence, func, select
from sqlalchemy.orm import Session

from c2s_challenge.common.protocol.dto import VehicleDto, VehicleFilterDto

from ..orm import VehicleORM
from . import DatabaseRepository


class VehicleRepository(DatabaseRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: VehicleDto) -> VehicleDto:
        orm: VehicleORM = VehicleORM(**entity.model_dump(exclude_none=True))

        self.session.add(orm)
        self.session.flush()

        self.session.refresh(orm)

        return VehicleDto.model_validate(orm, from_attributes=True)

    def search(
        self, filter: VehicleFilterDto, offset: int = 0, limit: int = 0
    ) -> tuple[list[VehicleDto], int]:
        search_query: Select[any] = self._make_select_filter(VehicleORM, filter)

        count_query: Select[any] = select(func.count()).select_from(
            search_query.subquery()
        )

        total: int = self.session.execute(count_query).scalar_one()

        search_query = search_query.offset(offset).limit(limit)

        results: Sequence = self.session.execute(search_query).scalars().all()

        return (results, total)
