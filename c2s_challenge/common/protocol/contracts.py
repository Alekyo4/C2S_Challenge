from enum import Enum
from http import HTTPStatus
from typing import Union

from pydantic import BaseModel, field_serializer

from .dto import VehicleChatIDto, VehicleChatODto, VehicleSearchIDto, VehicleSearchODto


class RequestEvent(Enum):
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
    status: HTTPStatus = HTTPStatus.OK

    data: Union[VehicleSearchODto, VehicleChatODto, str]
