from uuid import UUID, uuid4

from fastapi import UploadFile
from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, delete, and_

from src.db.models.car_attachment import CarAttachment


class CarAttachmentRepository(ISqlAlchemyRepository[CarAttachment]):
    _model = CarAttachment

    async def create_attachment(self, car_id: UUID, file: UploadFile) -> UUID:
        file_name = file.filename.split(".")
        new_file_name = f'{file_name[0]}-{uuid4()}.{file_name[-1]}'
        file.filename = new_file_name
        attachment = CarAttachment(
            car_id=car_id,
            attachment=file,
        )
        return await self.create(attachment)

    async def bulk_delete(self, car_id: UUID, obj_ids: list[UUID | int]) -> None:
        if not obj_ids:
            return

        result = await self.session.execute(
            select(self._model.id).where(and_(self._model.id.in_(obj_ids), self._model.car_id == car_id))
        )
        existing_ids = {row[0] for row in result.fetchall()}

        if not existing_ids:
            return

        await self.session.execute(delete(self._model).where(self._model.id.in_(existing_ids)))
