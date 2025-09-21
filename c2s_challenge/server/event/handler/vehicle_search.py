from c2s_challenge.common.protocol import Response
from c2s_challenge.common.protocol.dto import VehicleSearchIDto, VehicleSearchODto
from c2s_challenge.server.database.provider import DatabaseProvider
from c2s_challenge.server.database.repository import VehicleRepository

from ..provider import EventHandler


class VehicleSearchHandler(EventHandler):
    db: DatabaseProvider

    def __init__(self, database: DatabaseProvider):
        self.db = database

    async def handle(self, data: VehicleSearchIDto) -> Response:
        result: VehicleSearchODto = VehicleSearchODto(total=0, result=[])

        with self.db.get_session() as session:
            vehicle_repo: VehicleRepository = VehicleRepository(session=session)

            search_result, search_total = vehicle_repo.search(
                filter=data.filter, offset=data.offset, limit=data.limit
            )

            result = VehicleSearchODto(total=search_total, result=search_result)

        return Response(status="success", data=result)
