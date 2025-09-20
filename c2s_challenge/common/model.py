from pydantic import BaseModel, Field

from decimal import Decimal

from enum import Enum as PyEnum

class VehicleFuelType(PyEnum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"

class VehicleTransmission(PyEnum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"

class VehicleColor(PyEnum):
    BLACK = "black"
    WHITE = "white"
    SILVER = "silver"
    GRAY = "gray"
    BLUE = "blue"
    RED = "red"
    OTHER = "other"

class Vehicle(BaseModel):
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