from collections.abc import Sequence

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, and_, BinaryExpression, func
from sqlalchemy.orm import joinedload

from src.db.models.car import Car
from src.db.models.car_model import CarModel


class CarRepository(ISqlAlchemyRepository[Car]):
    _model = Car

    async def get_cars(
        self, conditions: list[BinaryExpression], limit: int = 30, offset: int = 0
    ) -> tuple[Sequence[Car], int]:
        base_query = select(Car).options(joinedload(Car.car_model).joinedload(CarModel.brand))
        if conditions:
            base_query = base_query.where(and_(*conditions))

        count_query = select(func.count()).select_from(base_query.subquery().alias("subq"))

        paginated_query = base_query.offset(offset).limit(limit)
        result = await self.session.execute(paginated_query)
        cars = result.unique().scalars().all()

        count_result = await self.session.execute(count_query)
        total = count_result.scalar()
        return cars, total
