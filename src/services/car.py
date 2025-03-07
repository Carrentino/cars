from uuid import UUID

from helpers.models.user import UserContext, UserStatus

from src.db.models.brand import Brand
from src.db.models.car import Car
from src.db.models.car_model import CarModel
from src.errors.service import UserIsNotVerifiedError, CarModelNotFoundError
from src.repositories.car import CarRepository
from src.repositories.car_model import CarModelRepository
from src.repositories.car_option import CarOptionRepository
from src.web.listings.schemas import CreateCarReq, CarFilters


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

    async def get_cars(self, filters: CarFilters):
        conditions = []
        if filters.car_id:
            if ',' in filters.car_id:
                conditions.append(Car.id.in_([UUID(item) for item in filters.car_id.split(',')]))
            else:
                conditions.append(Car.id == UUID(filters.car_id))
        if filters.color:
            if ',' in filters.color:
                conditions.append(Car.color.in_(filters.color.split(',')))
            else:
                conditions.append(Car.color == filters.color)
        if filters.car_model__title:
            if ',' in filters.car_model__title:
                conditions.append(CarModel.title.in_(filters.car_model__title.split(',')))
            else:
                conditions.append(CarModel.title == filters.car_model__title)
        if filters.brand__title:
            if ',' in filters.brand__title:
                conditions.append(Brand.title.in_(filters.brand__title.split(',')))
            else:
                conditions.append(Brand.title == filters.brand__title)
        if filters.price__gte is not None:
            conditions.append(Car.price >= filters.price__gte)
        if filters.price__lte is not None:
            conditions.append(Car.price <= filters.price__lte)
        if filters.score__gte is not None:
            conditions.append(Car.score >= filters.score__gte)
        if filters.score__lte is not None:
            conditions.append(Car.score <= filters.score__lte)
        if filters.date_from__gte is not None:
            conditions.append(Car.date_from >= filters.date_from__gte)
        if filters.date_from__lte is not None:
            conditions.append(Car.date_from <= filters.date_from__lte)
        if filters.date_to__gte is not None:
            conditions.append(Car.date_to >= filters.date_to__gte)
        if filters.date_to__lte is not None:
            conditions.append(Car.date_to <= filters.date_to__lte)
        if filters.car_model__hp__gte is not None:
            conditions.append(CarModel.hp >= filters.car_model__hp__gte)
        if filters.car_model__hp__lte is not None:
            conditions.append(CarModel.hp <= filters.car_model__hp__lte)
        if filters.car_model__engine_capacity__gte is not None:
            conditions.append(CarModel.engine_capacity >= filters.car_model__engine_capacity__gte)
        if filters.car_model__engine_capacity__lte is not None:
            conditions.append(CarModel.engine_capacity <= filters.car_model__engine_capacity__lte)
        if filters.car_model__fuel_consumption__gte is not None:
            conditions.append(CarModel.fuel_consumption >= filters.car_model__fuel_consumption__gte)
        if filters.car_model__fuel_consumption__lte is not None:
            conditions.append(CarModel.fuel_consumption <= filters.car_model__fuel_consumption__lte)
        return await self.car_repository.get_cars(conditions, filters.limit, filters.offset)
