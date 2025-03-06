from uuid import UUID

from fastapi import UploadFile
from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.car_attachment import CarAttachment
from src.settings import get_settings


class CarAttachmentRepository(ISqlAlchemyRepository[CarAttachment]):
    _model = CarAttachment

    async def create_attachment(self, car_id: UUID, file: UploadFile) -> UUID:
        file_path = get_settings().storage.save(file.file, file.filename)

        attachment = CarAttachment(
            car_id=car_id,
            attachment=file_path,
        )
        return await self.create(attachment)
