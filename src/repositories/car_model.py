from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.car_model import CarModel


class CarModelRepository(ISqlAlchemyRepository[CarModel]):
    _model = CarModel
