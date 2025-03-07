from typing import ClassVar
from uuid import UUID

from helpers.models.user import UserContext, UserStatus

from src.db.models.brand import Brand
from src.db.models.car import Car
from src.db.models.car_model import CarModel
from src.errors.service import UserIsNotVerifiedError, CarModelNotFoundError
from src.repositories.car import CarRepository
from src.repositories.car_model import CarModelRepository
from src.repositories.car_option import CarOptionRepository
from src.web.listings.schemas import CreateCarReq, CarFilters, BrandSchema, CarModelSchema, CarSchema


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
