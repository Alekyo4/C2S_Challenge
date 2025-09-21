from datetime import datetime

from typing import Literal, Optional, Union, List, Dict, Any

from pydantic import BaseModel, Field

class ChatMessageDto(BaseModel):
  role: Literal["user", "assistant"]

  date: datetime = Field(default_factory=datetime.now)

  content: str

  def __str__(self) -> str:
    return self.content

class VehicleFilterDto(BaseModel):
  make: Optional[str]

  model: Optional[str]

class VehicleSearchIDto(BaseModel):
  filter: VehicleFilterDto

class VehicleSearchODto(BaseModel):
  pass

class VehicleChatIDto(BaseModel):
  history: List[ChatMessageDto]

class VehicleChatODto(BaseModel):
  finished: bool

  content: Union[Dict[str, Any] | str]