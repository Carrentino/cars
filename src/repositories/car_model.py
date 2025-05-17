from collections.abc import Sequence
from uuid import UUID

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, func

from src.db.models.car_model import CarModel


class CarModelRepository(ISqlAlchemyRepository[CarModel]):
    _model = CarModel

    async def get_car_models(
        self, brand_ids: list[UUID], start: str = "", limit: int = 30, offset: int = 0
    ) -> tuple[Sequence[CarModel], int]:
        base_qry = select(CarModel).where(CarModel.title.istartswith(start))
        if brand_ids:
            base_qry = base_qry.where(CarModel.brand_id.in_(brand_ids))

        res_qry = base_qry.limit(limit).offset(offset)
        count_qry = select(func.count()).select_from(base_qry.subquery().alias("subq"))
        res = await self.session.execute(res_qry)
        car_models = res.unique().scalars().all()

        count_res = await self.session.execute(count_qry)
        total = count_res.scalar()
        return car_models, total
