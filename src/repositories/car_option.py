from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.car_option import CarOption


class CarOptionRepository(ISqlAlchemyRepository[CarOption]):
    _model = CarOption

    async def find_or_create_option(self, title: str) -> CarOption:
        option = await self.get_one_by(title=title)
        if not option:
            option = CarOption(title=title)
            await self.create(option)
        return option
