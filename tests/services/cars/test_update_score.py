from decimal import Decimal
from uuid import uuid4

import pytest

from src.errors.service import CarNotFoundError
from src.services.car import CarService
from tests.factories.car import CarFactory


async def test_update_score_ok(car_service: CarService) -> None:
    car = await CarFactory.create()
    await car_service.update_score(car.id, Decimal('4.0'))
    assert True


async def test_update_score_nf(car_service: CarService) -> None:
    with pytest.raises(CarNotFoundError):
        await car_service.update_score(uuid4(), Decimal('4.0'))
    assert True
