from typing import TYPE_CHECKING

from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from src.db.models.car_model import CarModel


class Brand(Base):
    __tablename__ = 'brands'

    title: Mapped[str]

    car_models: Mapped[list["CarModel"]] = relationship("CarModel",
                                                        back_populates="brand")
