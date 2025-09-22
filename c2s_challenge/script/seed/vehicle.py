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
            vehicles: list[VehicleDto] = [self.faker.create() for _ in range(num)]

            vehicle_repo: VehicleRepository = VehicleRepository(session=session)

            for index, vehicle in enumerate(vehicles):
                vehicle_repo.add(vehicle)

                self.logger.debug(f"Vehicle {index + 1} added successfully")

            session.commit()
