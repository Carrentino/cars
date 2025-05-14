from sqladmin import ModelView

from src.db.models.car import Car


class CarAdmin(ModelView, model=Car):
    column_list = [Car.id, Car.car_model, Car.owner_id]  # noqa: RUF012
