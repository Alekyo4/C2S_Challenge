from pydantic import BaseModel, Field

class VehicleSearchIDto(BaseModel):
  make: str = Field(min_length=1, max_length=50)

  model: str = Field(min_length=1, max_length=50)

class VehicleSearchODto(BaseModel):
  id: str

  make: str