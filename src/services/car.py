from uuid import UUID

from helpers.models.user import UserContext, UserStatus

from src.db.models.car import Car
from src.errors.service import UserIsNotVerifiedError, CarModelNotFoundError
from src.repositories.car import CarRepository
from src.repositories.car_model import CarModelRepository
from src.repositories.car_option import CarOptionRepository
from src.web.listings.schemas import CreateCarReq


class CarService:
    def __init__(
        self,
        car_repository: CarRepository,
        car_model_repository: CarModelRepository,
        car_option_repository: CarOptionRepository,
    ) -> None:
        self.car_model_repository = car_model_repository
        self.car_repository = car_repository
        self.car_option_repository = car_option_repository

    async def create_car(self, user: UserContext, req: CreateCarReq) -> UUID:
        if user.status == UserStatus.NOT_VERIFIED:
            raise UserIsNotVerifiedError
        car_model = await self.car_model_repository.get(UUID(req.car_model_id))
        if car_model is None:
            raise CarModelNotFoundError
        options = [await self.car_option_repository.find_or_create_option(option.title) for option in req.options]
        car = Car(
            car_model_id=UUID(req.car_model_id),
            color=req.color,
            price=req.price,
            owner_id=UUID(user.user_id),
            latitude=req.latitude,
            longitude=req.longitude,
            date_from=req.date_from,
            date_to=req.date_to,
            car_options=options,
        )
        car_id = await self.car_repository.create(car)
        return car_id
