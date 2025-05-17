from collections.abc import Sequence

from src.db.models.brand import Brand
from src.repositories.brand import BrandRepository


class BrandService:
    def __init__(self, brand_repository: BrandRepository) -> None:
        self.brand_repository = brand_repository

    async def get_brands(self, start: str = "", limit: int = 30, offset: int = 0) -> tuple[Sequence[Brand], int]:
        return await self.brand_repository.get_brands(start, limit, offset)
