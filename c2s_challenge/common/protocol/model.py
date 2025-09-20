from pydantic import BaseModel, field_serializer

from typing import Literal, Union

from enum import Enum as PyEnum

from .dto import VehicleSearchIDto, VehicleSearchODto

class RequestEvent(PyEnum):
  VEHICLE_SEARCH = ("vehicle-search", VehicleSearchIDto)

  def __init__(self, name: str, dto: type[BaseModel]):
    self.evt_name = name
    self.dto_class = dto

class Request(BaseModel):
  event: RequestEvent

  data: Union[VehicleSearchIDto]

  @field_serializer("event")
  def serialize_event(self, event: RequestEvent) -> str:
    return event.evt_name

class Response(BaseModel):
  status: Literal["success", "error"]

  data: Union[VehicleSearchODto, str]