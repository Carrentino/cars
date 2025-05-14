from sqladmin import ModelView

from src.db.models.car_option import CarOption


class CarOptionAdmin(ModelView, model=CarOption):
    column_list = [CarOption.id, CarOption.title]  # noqa: RUF012
