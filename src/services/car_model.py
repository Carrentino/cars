from collections.abc import Sequence
from uuid import UUID

from src.db.models.car_model import CarModel
from src.repositories.car_model import CarModelRepository


class CarModelService:
    def __init__(self, car_model_repository: CarModelRepository) -> None:
        self.car_model_repository = car_model_repository

    async def get_car_models(
        self, brand_ids: list[UUID], start: str = "", limit: int = 30, offset: int = 0
    ) -> tuple[Sequence[CarModel], int]:
        return await self.car_model_repository.get_car_models(start, brand_ids, limit, offset)
