from sqladmin import ModelView

from src.db.models.car_model import CarModel


class CarModelAdmin(ModelView, model=CarModel):
    column_list = [CarModel.id, CarModel.brand, CarModel.title]  # noqa: RUF012
