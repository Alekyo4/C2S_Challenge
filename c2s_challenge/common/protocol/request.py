from pydantic import BaseModel

from typing import NamedTuple, Literal

from enum import Enum as PyEnum

from .dto import VehicleSearchDto

type EventMapper = tuple[str, type[BaseModel]]

class RequestEvent(PyEnum):
  VEHICLE_SEARCH: EventMapper = ("vehicle-search", VehicleSearchDto)

  def __init__(self, name: str, dto: type[BaseModel]):
    self.evt_name = name

    self.dto = dto

class Request(NamedTuple):
  event: RequestEvent

  data: BaseModel

class Response(BaseModel):
  status: Literal["sucess", "error"]

  data: type[BaseModel] | str