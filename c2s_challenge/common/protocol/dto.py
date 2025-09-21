from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class VehicleFuelType(Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"


class VehicleTransmission(Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class VehicleColor(Enum):
    BLACK = "black"
    WHITE = "white"
    SILVER = "silver"
    GRAY = "gray"
    BLUE = "blue"
    RED = "red"
    OTHER = "other"


class VehicleDto(BaseModel):
    """
    Represents the business entity of a Vehicle.
    Validates and types data robustly.
    """

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

    created_at: str | None = None
    updated_at: str | None = None

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
    make: Optional[str] = None

    model: Optional[str] = None

    vin: Optional[str] = None

    engine: Optional[str] = None

    fuel_type: Optional[VehicleFuelType] = None

    transmission: Optional[VehicleTransmission] = None

    color: Optional[VehicleColor] = None

    color_detail: Optional[str] = None

    price: Optional[float] = None

    min_price: Optional[Decimal] = None

    max_price: Optional[Decimal] = None

    doors: Optional[int] = None

    min_doors: Optional[int] = None

    max_doors: Optional[int] = None

    mileage: Optional[int] = None

    min_mileage: Optional[int] = None

    max_mileage: Optional[int] = None

    year: Optional[int] = None

    min_year: Optional[int] = None

    max_year: Optional[int] = None


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
