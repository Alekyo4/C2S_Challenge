from decimal import Decimal

from faker import Faker
from faker.providers import automotive

from c2s_challenge.common.protocol.dto import (
    VehicleColor,
    VehicleDto,
    VehicleFuelType,
    VehicleTransmission,
)

from .provider import FakerProvider


class VehicleFaker(FakerProvider[VehicleDto]):
    faker: Faker

    elements: dict[str, any] = {
        "make": ["fiat", "ford", "vw", "chevrolet", "toyota"],
        "model": {
            "fiat": ["uno", "palio", "500"],
            "ford": ["fiesta", "focus", "mustang"],
            "vw": ["golf", "polo", "tiguan"],
            "chevrolet": ["onix", "cruze", "camaro"],
            "toyota": ["corolla", "yaris", "hilux"],
        },
        "doors": [2, 4, 6],
    }

    def __init__(self, faker: Faker):
        self.faker = faker

        self.faker.add_provider(automotive)

    def __make_engine(self) -> str:
        return f"{self.faker.random_int(1, 8)} {self.faker.random_int(0, 9)}L {self.faker.random_element(['V', 'I'])}-Cylinder"

    def create(self) -> VehicleDto:
        make: str = self.faker.random_element(elements=self.elements["make"])

        color_detail: str = (
            self.faker.color_name() if self.faker.random_digit() >= 5 else None
        )

        return VehicleDto(
            make=make,
            model=self.faker.random_element(self.elements["model"][make]),
            vin=self.faker.unique.vin(),
            engine=self.__make_engine(),
            fuel_type=self.faker.random_element(list(VehicleFuelType)),
            transmission=self.faker.random_element(list(VehicleTransmission)),
            color=self.faker.random_element(list(VehicleColor)),
            color_detail=color_detail,
            price=Decimal(self.faker.random_int(5000, 100_000)),
            doors=self.faker.random_element(self.elements["doors"]),
            mileage=self.faker.random_int(0, 300_000),
            year=self.faker.random_int(1900, 2025),
        )
