from faker import Faker
from typer import Typer

from c2s_challenge.common.setting.setting import Setting
from c2s_challenge.script.faker.vehicle import VehicleFaker
from c2s_challenge.server.database.database import Database

from .seed import VehicleSeeder

cli: Typer = Typer()

faker: Faker = Faker()


@cli.command("vehicle")
def seed_vehicle(num: int):
    setting: Setting = Setting()

    database: Database = Database(setting=setting)

    vehicle_faker: VehicleFaker = VehicleFaker(faker=faker)

    VehicleSeeder(database=database, faker=vehicle_faker).run(num)


if __name__ == "__main__":
    cli()
