from uuid import UUID

from fastapi import UploadFile
from helpers.models.user import UserContext, UserStatus

from src.db.models.car import Car
from src.errors.service import UserIsNotVerifiedError
from src.repositories.car import CarRepository
from src.repositories.car_attachment import CarAttachmentRepository
from src.repositories.car_option import CarOptionRepository
from src.web.listings.schemas import CreateCarReq


class CarService:
    def __init__(
        self,
        car_repository: CarRepository,
        car_attachment_repository: CarAttachmentRepository,
        car_option_repository: CarOptionRepository
    ) -> None:
        self.car_repository = car_repository
        self.car_attachment_repository = car_attachment_repository
        self.car_option_repository = car_option_repository

    async def create_car(self, user: UserContext, req: CreateCarReq,
                         attachments: list[UploadFile]) -> UUID:
        if user.status == UserStatus.NOT_VERIFIED:
            raise UserIsNotVerifiedError
        car = Car(
            car_model_id=req.car_model_id,
            color=req.color,
            owner_id=user.user_id,
            latitude=req.latitude,
            longitude=req.longitude,
            date_from=req.date_from,
            date_to=req.date_to,
        )
        car_id = await self.car_repository.create(car)
        options = [await self.car_option_repository.find_or_create_option(option.title)
                   for option in
                   req.options]
        car.car_options.extend(options)
        await self.car_repository.update_object(car)
        for attachment in attachments:
            await self.car_attachment_repository.create_attachment(car_id, attachment)

        return car_id
