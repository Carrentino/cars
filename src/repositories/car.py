from collections.abc import Sequence

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, and_, BinaryExpression
from sqlalchemy.orm import joinedload

from src.db.models.car import Car
from src.db.models.car_model import CarModel


class CarRepository(ISqlAlchemyRepository[Car]):
    _model = Car

    async def get_cars(self, conditions: list[BinaryExpression], limit: int = 30, offset: int = 0) -> Sequence[Car]:
        query = select(Car).options(joinedload(Car.car_model).joinedload(CarModel.brand))
        if conditions:
            query = query.where(and_(*conditions))

        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.unique().scalars().all()
