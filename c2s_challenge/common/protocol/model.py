from pydantic import BaseModel, field_serializer

from typing import Literal, Union

from enum import Enum as PyEnum

from .dto import VehicleSearchIDto, VehicleSearchODto, VehicleChatIDto, VehicleChatODto


class RequestEvent(PyEnum):
    VEHICLE_SEARCH = ("vehicle-search", VehicleSearchIDto)

    VEHICLE_CHAT = ("vehicle-search-chat", VehicleChatIDto)

    def __init__(self, name: str, dto: type[BaseModel]):
        self.evt_name = name
        self.dto_class = dto


class Request(BaseModel):
    event: RequestEvent

    data: Union[VehicleSearchIDto, VehicleChatIDto]

    @field_serializer("event")
    def serialize_event(self, event: RequestEvent) -> str:
        return event.evt_name


class Response(BaseModel):
    status: Literal["success", "error"]

    data: Union[VehicleSearchODto, VehicleChatODto, str]
