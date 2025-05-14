from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import ForeignKey, Enum, UniqueConstraint, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enums.car import CarStatus
from src.db.models.associatoins import car_options_association

if TYPE_CHECKING:
    from src.db.models.car_model import CarModel
    from src.db.models.car_option import CarOption
    from src.db.models.car_attachment import CarAttachment


class Car(Base):
    __tablename__ = 'cars'
    __table_args__ = (
        UniqueConstraint('vin', 'license_plate', name='uq_car_vin_license'),
        Index('idx_car_model', 'car_model_id'),
        Index('idx_owner_id', 'owner_id'),
        Index('idx_status', 'status'),
        Index('idx_price', 'price'),
        CheckConstraint('score >= 0 AND score <= 5', name='chk_car_score'),
        CheckConstraint('price >= 0', name='chk_car_price'),
    )

    car_model_id: Mapped[UUID] = mapped_column(ForeignKey('car_models.id', ondelete='RESTRICT'), nullable=False)
    color: Mapped[str]
    score: Mapped[Decimal] = mapped_column(default=5.0)
    vin: Mapped[str]
    license_plate: Mapped[str]
    price: Mapped[int]
    owner_id: Mapped[UUID]
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus), default=CarStatus.NOT_VERIFIED)
    latitude: Mapped[str]
    longitude: Mapped[str]
    date_from: Mapped[datetime] = mapped_column(nullable=True)
    date_to: Mapped[datetime] = mapped_column(nullable=True)

    car_model: Mapped["CarModel"] = relationship("CarModel", back_populates="cars", passive_deletes=True)
    options: Mapped[list["CarOption"]] = relationship(
        "CarOption", secondary=car_options_association, back_populates="cars"
    )
    attachments: Mapped[list["CarAttachment"]] = relationship("CarAttachment", back_populates="car")

    def __repr__(self):
        return str(self.id)
