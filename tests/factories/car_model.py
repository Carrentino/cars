import factory

from src.db.enums.car_model import CarModelDrive, CarModelGearbox, CarModelBody, CarModelFuel
from src.db.models.car_model import CarModel
from tests.factories.base import BaseSqlAlchemyFactory


class CarModelFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = CarModel

    title = factory.Faker('word')
    brand = factory.SubFactory("tests.factories.brand.BrandFactory")
    drive = factory.Iterator(CarModelDrive)
    gearbox = factory.Iterator(CarModelGearbox)
    body = factory.Iterator(CarModelBody)
    fuel = factory.Iterator(CarModelFuel)
    fuel_consumption = factory.Faker('pydecimal', left_digits=2, right_digits=1, positive=True)
    hp = factory.Faker('random_int', min=1, max=1000)
    engine_capacity = factory.Faker('pydecimal', left_digits=1, right_digits=1, positive=True)
