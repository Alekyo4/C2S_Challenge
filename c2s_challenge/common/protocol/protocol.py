from json import JSONDecodeError
from json import loads as loads_json

from pydantic import BaseModel, ValidationError

from .contracts import Request, RequestEvent, Response
from .exception import (
    ProtocolNotFoundEvent,
    ProtocolRequestInvalid,
    ProtocolResponseInvalid,
)


class Protocol:
    @staticmethod
    def parse_request(payload: dict[str, any] | bytes) -> Request:
        try:
            if isinstance(payload, bytes):
                request_raw: dict[str, any] = loads_json(payload.decode("utf-8"))
            else:
                request_raw: dict[str, any] = payload

            event_name: str = request_raw.get("event")

            if not event_name:
                raise ProtocolRequestInvalid()

            event: RequestEvent | None = next(
                (evt for evt in RequestEvent if evt.evt_name == event_name), None
            )

            if not event:
                raise ProtocolNotFoundEvent()

            validate: BaseModel = event.dto_class.model_validate(
                request_raw.get("data", {})
            )

            return Request(event=event, data=validate)
        except (ValidationError, JSONDecodeError, ValueError):
            raise ProtocolRequestInvalid()

    @staticmethod
    def parse_response(payload: bytes) -> Response:
        try:
            return Response.model_validate_json(payload.decode("utf-8"))
        except (ValidationError, JSONDecodeError, ValueError):
            raise ProtocolResponseInvalid()
