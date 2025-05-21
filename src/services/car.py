from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from helpers.models.user import UserContext

from src.db.enums.car import CarStatus
from src.db.models.brand import Brand
from src.db.models.car import Car
from src.db.models.car_model import CarModel
from src.errors.service import CarModelNotFoundError, CarNotFoundError, UserIsNotOwnerError
from src.integrations.reviews import ReviewsClient
from src.repositories.car import CarRepository
from src.repositories.car_model import CarModelRepository
from src.repositories.car_option import CarOptionRepository
from src.utils import encrypt_data
from src.web.api.listings.schemas import (
    CreateCarReq,
    CarFilters,
    BrandSchema,
    CarModelSchema,
    CarSchema,
    RetrieveCarSchema,
    UpdateCarSchema,
)


class CarService:
    prefix_model: ClassVar = {
        'car__': Car,
        'car_model__': CarModel,
        'brand__': Brand,
    }

    def __init__(
        self,
        car_repository: CarRepository,
        car_model_repository: CarModelRepository,
        car_option_repository: CarOptionRepository,
        reviews_client: ReviewsClient,
    ) -> None:
        self.car_model_repository = car_model_repository
        self.car_repository = car_repository
        self.car_option_repository = car_option_repository
        self.reviews_client = reviews_client

    async def get_current_car(
        self, car_id: UUID, user: UserContext | None, token: str | None = None
    ) -> RetrieveCarSchema:
        car = await self.car_repository.get_car_by_id(car_id)
        if car is None:
            raise CarNotFoundError
        if user is None and car.status != CarStatus.VERIFIED:
            raise CarNotFoundError
        if user is not None and UUID(user.user_id) != car.owner_id and car.status != CarStatus.VERIFIED:
            raise CarNotFoundError
        reviews = await self.reviews_client.get_reviews(car_id, token)
        car.reviews = reviews
        return RetrieveCarSchema.model_validate(
            car,
            from_attributes=True,
        )

    async def create_car(self, user: UserContext, req: CreateCarReq) -> UUID:
        # if user.status == UserStatus.NOT_VERIFIED:
        #     raise UserIsNotVerifiedError
        car_model = await self.car_model_repository.get(UUID(req.car_model_id))
        if car_model is None:
            raise CarModelNotFoundError
        options = [await self.car_option_repository.find_or_create_option(option.title) for option in req.options]
        car = Car(
            car_model_id=UUID(req.car_model_id),
            color=req.color,
            price=req.price,
            owner_id=UUID(user.user_id),
            vin=encrypt_data(req.vin),
            license_plate=encrypt_data(req.license_plate),
            latitude=req.latitude,
            longitude=req.longitude,
            date_from=req.date_from,
            date_to=req.date_to,
            options=options,
        )
        car_id = await self.car_repository.create(car)
        return car_id

    async def get_cars(self, filters: CarFilters):
        conditions = []
        for filter_name, value in filters.dict().items():
            if value is None or filter_name in ('limit', 'offset'):
                continue
            parts = filter_name.split('__')
            attr_name = parts[1]
            for prefix, model in self.prefix_model.items():
                if filter_name.startswith(prefix):
                    field = getattr(model, attr_name)
                    break
            else:
                field = None
            if field is not None:
                if isinstance(value, list):
                    conditions.append(field.in_(value))
                elif parts[-1] == 'gte':
                    conditions.append(field >= value)
                elif parts[-1] == 'lte':
                    conditions.append(field <= value)
                else:
                    conditions.append(field == value)
        result, count = await self.car_repository.get_cars(conditions, filters.limit, filters.offset)
        clean_result = []
        for item in result:
            brand = BrandSchema.model_validate(item.car_model.brand)
            car_model = CarModelSchema.model_validate(item.car_model, context={'brand': brand})

            car = CarSchema.model_validate(item, context={'car_model': car_model})
            clean_result.append(car)
        return clean_result, count

    async def delete_car(self, user_id: UUID, car_id: UUID) -> None:
        car = await self.car_repository.get(car_id)
        if car is None:
            raise CarNotFoundError
        if car.owner_id != user_id:
            raise UserIsNotOwnerError
        await self.car_repository.delete(car_id)

    async def update_car(self, user_id: UUID, car_id: UUID, req: UpdateCarSchema) -> None:
        car = await self.car_repository.get(car_id)
        if car is None:
            raise CarNotFoundError
        if car.owner_id != user_id:
            raise UserIsNotOwnerError
        update_data = req.model_dump(mode='python')
        update_data['status'] = CarStatus.NOT_VERIFIED
        update_data['options'] = [
            await self.car_option_repository.find_or_create_option(option.title) for option in req.options
        ]
        for k, v in update_data.items():
            if k in car.__dict__:
                setattr(car, k, v)
        await self.car_repository.update_object(car)

    async def update_score(self, car_id: UUID, score: Decimal) -> None:
        car = await self.car_repository.get(car_id)
        if car is None:
            raise CarNotFoundError
        car.score = score
        await self.car_repository.update_object(car)
