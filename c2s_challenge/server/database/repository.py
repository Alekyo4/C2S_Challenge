from c2s_challenge.core import Vehicle as VehicleModel

from .orm import VehicleORM

from .abstract import DatabaseProvider

class VehicleRepository:
  db: DatabaseProvider

  def __init__(self, database: DatabaseProvider):
    self.db = database

  def add(self, vehicle: VehicleModel) -> VehicleModel:
    orm: VehicleORM = VehicleORM(**vehicle.model_dump(exclude_none=True))

    with self.db.get_session() as ses:
      ses.add(orm)
      ses.commit()

      ses.refresh(orm)

    return VehicleModel.model_validate(orm)