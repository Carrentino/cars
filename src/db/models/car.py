from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enums.car import CarStatus
from src.db.models.associatoins import car_options_association

if TYPE_CHECKING:
    from src.db.models.car_model import CarModel
    from src.db.models.car_option import CarOption
    from src.db.models.car_attachment import CarAttachment


class Car(Base):
    __tablename__ = 'cars'

    car_model_id: Mapped[UUID] = mapped_column(ForeignKey('car_models.id'), nullable=False)
    color: Mapped[str]
    score: Mapped[Decimal] = mapped_column(default=5.0)
    price: Mapped[int]
    owner_id: Mapped[UUID]
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus), default=CarStatus.NOT_VERIFIED)
    latitude: Mapped[str]
    longitude: Mapped[str]
    date_from: Mapped[datetime] = mapped_column(nullable=True)
    date_to: Mapped[datetime] = mapped_column(nullable=True)

    car_model: Mapped["CarModel"] = relationship("CarModel", back_populates="cars")
    options: Mapped[list["CarOption"]] = relationship(
        "CarOption", secondary=car_options_association, back_populates="cars"
    )
    attachments: Mapped[list["CarAttachment"]] = relationship("CarAttachment", back_populates="car")
