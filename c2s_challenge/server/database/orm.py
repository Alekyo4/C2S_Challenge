from decimal import Decimal

from sqlalchemy import DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from ulid import ULID

from c2s_challenge.common.protocol.dto import (
    VehicleColor,
    VehicleFuelType,
    VehicleTransmission,
)


class BaseORM(DeclarativeBase):
    pass


class VehicleORM(BaseORM):
    __tablename__ = "vehicles"

    id: Mapped[str] = mapped_column(
        String(26), primary_key=True, default=lambda: str(ULID())
    )

    make: Mapped[str] = mapped_column(String(50), nullable=False)

    model: Mapped[str] = mapped_column(String(50), nullable=False)

    vin: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)

    engine: Mapped[str] = mapped_column(String(50), nullable=False)

    fuel_type: Mapped[VehicleFuelType] = mapped_column(
        Enum(VehicleFuelType, name="vehiclefueltype"), nullable=False
    )

    transmission: Mapped[VehicleTransmission] = mapped_column(
        Enum(VehicleTransmission, name="vehicletransmission"), nullable=False
    )

    color: Mapped[VehicleColor] = mapped_column(
        Enum(VehicleColor, name="vehiclecolor"), nullable=False
    )

    color_detail: Mapped[str | None] = mapped_column(String(50), nullable=True)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    doors: Mapped[int] = mapped_column(Integer, nullable=False)

    mileage: Mapped[int] = mapped_column(Integer, nullable=False)

    year: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Vehicle(id={self.id}, make='{self.make}', model='{self.model}')>"
