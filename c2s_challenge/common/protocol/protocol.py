from pydantic import ValidationError, BaseModel

from json import JSONDecodeError, loads as loads_json

from .exception import ProtocolNotFoundEvent, ProtocolResponseInvalid, ProtocolRequestInvalid

from .model import RequestEvent, Request, Response

class Protocol:
  @staticmethod
  def parse_request(payload: bytes) -> Request:
    try:
      raw: dict[str, any] = loads_json(payload.decode('utf-8'))
      
      event_name: str = raw.get('event')

      if not event_name:
        raise ProtocolRequestInvalid()
      
      event: RequestEvent | None = next(
        (evt for evt in RequestEvent if evt.evt_name == event_name), None)

      if not event:
        raise ProtocolNotFoundEvent()

      validate: BaseModel = event.dto_class.model_validate(raw.get("data", { }))
      
      return Request(event=event, data=validate)
    except (ValidationError, JSONDecodeError, ValueError):
      raise ProtocolRequestInvalid()
  
  @staticmethod
  def parse_response(payload: bytes) -> Response:
    try:
      return Response.model_validate_json(payload.decode("utf-8"))
    except (ValidationError, JSONDecodeError, ValueError):
      raise ProtocolResponseInvalid()