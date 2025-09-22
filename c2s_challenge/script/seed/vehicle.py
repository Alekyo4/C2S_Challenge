from c2s_challenge.common.logger import Logger, get_logger
from c2s_challenge.common.protocol.dto import VehicleDto
from c2s_challenge.script.faker.provider import FakerProvider
from c2s_challenge.server.database.provider import DatabaseProvider
from c2s_challenge.server.database.repository.vehicle import VehicleRepository

from .provider import SeederProvider


class VehicleSeeder(SeederProvider[VehicleDto]):
    database: DatabaseProvider

    logger: Logger = get_logger("VehicleSeeder")

    def __init__(self, database: DatabaseProvider, faker: FakerProvider[VehicleDto]):
        self.faker = faker

        self.database = database

    def run(self, num: int) -> None:
        with self.database.get_session() as session:
            for vehicle_index in range(num):
                vehicle: VehicleDto = self.faker.create()

                vehicle_repo: VehicleRepository = VehicleRepository(session=session)

                vehicle_repo.add(vehicle)

                self.logger.debug(f"Vehicle {vehicle_index + 1} added successfully")
