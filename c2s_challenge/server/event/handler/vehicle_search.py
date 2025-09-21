from c2s_challenge.common.protocol import Response

from c2s_challenge.common.protocol.dto import VehicleSearchIDto, VehicleSearchODto

from c2s_challenge.server.database import VehicleRepository

from ..abstract import EventHandler


class VehicleSearchHandler(EventHandler):
    repository: VehicleRepository

    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    async def handle(self, data: VehicleSearchIDto) -> Response:
        result: VehicleSearchODto = VehicleSearchODto()

        return Response(status="success", data=result)
