from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class VehicleFuelType(Enum):
    GASOLINE = "GASOLINE"
    DIESEL = "DIESEL"
    ELECTRIC = "ELECTRIC"
    HYBRID = "HYBRID"


class VehicleTransmission(Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"


class VehicleColor(Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"
    SILVER = "SILVER"
    GRAY = "GRAY"
    BLUE = "BLUE"
    RED = "RED"
    OTHER = "OTHER"


class VehicleDto(BaseModel):
    id: str | None = None

    make: str = Field(min_length=1, max_length=50)

    model: str = Field(min_length=1, max_length=50)

    vin: str = Field(min_length=17, max_length=17)

    engine: str = Field(min_length=1, max_length=50)

    fuel_type: VehicleFuelType

    transmission: VehicleTransmission

    color: VehicleColor

    color_detail: str | None = None

    price: Decimal = Field(gt=0)

    doors: int = Field(gt=0)

    mileage: int = Field(ge=0)

    year: int = Field(ge=1900)

    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        use_enum_values = True
        from_attributes = True


class ChatMessageDto(BaseModel):
    role: Literal["user", "assistant"]

    date: datetime = Field(default_factory=datetime.now)

    content: str

    def __str__(self) -> str:
        return self.content


class VehicleFilterDto(BaseModel):
    make: Optional[str]

    model: Optional[str]

    vin: Optional[str]

    engine: Optional[str]

    fuel_type: Optional[VehicleFuelType]

    transmission: Optional[VehicleTransmission]

    color: Optional[VehicleColor]

    color_detail: Optional[str]

    price: Optional[float]

    min_price: Optional[float]

    max_price: Optional[float]

    doors: Optional[int]

    min_doors: Optional[int]

    max_doors: Optional[int]

    mileage: Optional[int]

    min_mileage: Optional[int]

    max_mileage: Optional[int]

    year: Optional[int]

    min_year: Optional[int]

    max_year: Optional[int]


class VehicleSearchIDto(BaseModel):
    filter: VehicleFilterDto

    offset: int = Field(0, gte=0)

    limit: int = Field(5, gt=0, lte=100)


class VehicleSearchODto(BaseModel):
    total: int

    result: list[VehicleDto]


class VehicleChatIDto(BaseModel):
    history: List[ChatMessageDto]


class VehicleChatODto(BaseModel):
    type: Literal["text", "filter"]

    content: Union[VehicleFilterDto, str]
