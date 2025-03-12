from typing import TYPE_CHECKING
from uuid import UUID

from fastapi_storages.integrations.sqlalchemy import FileType
from helpers.sqlalchemy.base_model import Base
from sqlalchemy import ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.settings import get_settings

if TYPE_CHECKING:
    from src.db.models.car import Car


class CarAttachment(Base):
    __tablename__ = 'car_attachments'
    car_id: Mapped[UUID] = mapped_column(ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    attachment: Mapped[FileType] = mapped_column(FileType(storage=get_settings().storage), nullable=False)

    car: Mapped["Car"] = relationship("Car", back_populates="attachments")


@event.listens_for(CarAttachment, 'before_delete')
def delete_file(mapper, connection, target):  # noqa: ARG001
    storage = target.attachment.storage
    storage.delete(target.attachment.name)
