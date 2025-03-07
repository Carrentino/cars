from uuid import uuid4

import factory

from src.db.enums.car import CarStatus
from src.db.models.car import Car
from tests.factories.base import BaseSqlAlchemyFactory


class CarFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = Car

    car_model = factory.SubFactory('tests.factories.car_model.CarModelFactory')
    color = factory.Faker('color')
    score = factory.Faker('pydecimal', left_digits=1, right_digits=1, positive=True)
    price = factory.Faker('random_int', min=1000, max=10000)
    owner_id = factory.LazyAttribute(lambda _: uuid4())
    status = factory.Iterator(CarStatus)
    latitude = factory.Faker('word')
    longitude = factory.Faker('word')
