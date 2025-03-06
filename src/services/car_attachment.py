from uuid import UUID

from fastapi import UploadFile
from helpers.models.user import UserContext

from src.errors.service import CarNotFoundError, UserIsNotOwnerError
from src.repositories.car import CarRepository
from src.repositories.car_attachment import CarAttachmentRepository


class CarAttachmentService:

    def __init__(
        self,
        car_attachment_repository: CarAttachmentRepository,
        car_repository: CarRepository,
    ) -> None:
        self.car_attachment_repository = car_attachment_repository
        self.car_repository = car_repository

    async def add_attachments(self, user_context: UserContext, car_id: UUID, attachments: list[UploadFile]) -> None:
        car = await self.car_repository.get(car_id)
        if car is None:
            raise CarNotFoundError
        if car.owner_id != user_context.user_id:
            raise UserIsNotOwnerError
        for attachment in attachments:
            await self.car_attachment_repository.create_attachment(car_id, attachment)
