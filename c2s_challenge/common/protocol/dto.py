from datetime import datetime

from typing import Literal, List

from pydantic import BaseModel, Field

class ChatMessageDto(BaseModel):
  role: Literal["user", "assistant"]

  date: datetime = Field(default_factory=datetime.now)

  content: str

  def __str__(self) -> str:
    return self.content

class VehicleSearchIDto(BaseModel):
  make: str = Field(min_length=1, max_length=50)

  model: str = Field(min_length=1, max_length=50)

class VehicleSearchChatIDto(BaseModel):
  history: List[ChatMessageDto]

class VehicleSearchODto(BaseModel):
  pass

class VehicleSearchChatODto(BaseModel):
  finished: bool
  content: str