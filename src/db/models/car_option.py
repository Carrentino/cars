from typing import TYPE_CHECKING

from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped, relationship

from src.db.models.associatoins import car_options_association

if TYPE_CHECKING:
    from src.db.models.car import Car


class CarOption(Base):
    __tablename__ = "car_options"
    title: Mapped[str]

    cars: Mapped[list["Car"]] = relationship("Car", secondary=car_options_association, back_populates="options")

    def __repr__(self):
        return self.title
