from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enums.car_model import CarModelDrive, CarModelGearbox, CarModelBody, CarModelFuel

if TYPE_CHECKING:
    from src.db.models.brand import Brand
    from src.db.models.car import Car


class CarModel(Base):
    __tablename__ = 'car_models'
    __table_args__ = (
        Index('idx_car_model_title', 'title'),
        Index('idx_car_model_brand_id', 'brand_id'),
        Index('idx_car_model_hp', 'hp'),
    )

    title: Mapped[str]
    brand_id: Mapped[UUID] = mapped_column(ForeignKey('brands.id', ondelete='RESTRICT'), nullable=True)
    drive: Mapped[CarModelDrive] = mapped_column(Enum(CarModelDrive), nullable=False)
    gearbox: Mapped[CarModelGearbox] = mapped_column(Enum(CarModelGearbox), nullable=False)
    body: Mapped[CarModelBody] = mapped_column(Enum(CarModelBody), nullable=False)
    fuel: Mapped[CarModelFuel] = mapped_column(Enum(CarModelFuel), nullable=False)
    fuel_consumption: Mapped[Decimal]
    hp: Mapped[int]
    engine_capacity: Mapped[Decimal]

    brand: Mapped["Brand"] = relationship("Brand", back_populates="car_models", passive_deletes=True)
    cars: Mapped[list["Car"]] = relationship("Car", back_populates="car_model")

    def __str__(self):
        return self.title
