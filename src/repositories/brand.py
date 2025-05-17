from collections.abc import Sequence

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, func

from src.db.models.brand import Brand


class BrandRepository(ISqlAlchemyRepository[Brand]):
    _model = Brand

    async def get_brands(self, start: str = "", limit: int = 30, offset: int = 0) -> tuple[Sequence[Brand], int]:
        base_qry = select(Brand).where(Brand.title.istartswith(start))

        res_qry = base_qry.limit(limit).offset(offset)
        count_qry = select(func.count()).select_from(base_qry.subquery().alias("subq"))
        res = await self.session.execute(res_qry)
        brands = res.unique().scalars().all()

        count_res = await self.session.execute(count_qry)
        total = count_res.scalar()
        return brands, total
