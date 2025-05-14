from typing import TYPE_CHECKING

from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from src.db.models.car_model import CarModel


class Brand(Base):
    __tablename__ = 'brands'

    title: Mapped[str] = mapped_column(unique=True)

    car_models: Mapped[list["CarModel"]] = relationship("CarModel", back_populates="brand")

    def __repr__(self):
        return self.title
