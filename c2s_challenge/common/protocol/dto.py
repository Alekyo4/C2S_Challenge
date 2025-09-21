from datetime import datetime
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from c2s_challenge.common import Vehicle


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

    start: int = Field(min_length=0)

    limit: int = Field(min_length=0, max_length=100)


class VehicleSearchODto(BaseModel):
    result: Vehicle

    length: int


class VehicleChatIDto(BaseModel):
    history: List[ChatMessageDto]


class VehicleChatODto(BaseModel):
    type: Literal["text", "filter"]

    content: Union[VehicleFilterDto, str]
