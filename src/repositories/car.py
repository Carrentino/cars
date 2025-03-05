from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.car import Car


class CarRepository(ISqlAlchemyRepository[Car]):
    _model = Car
