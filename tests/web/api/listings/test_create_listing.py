from uuid import uuid4

from httpx import AsyncClient
from starlette import status

from tests.factories.car_model import CarModelFactory


async def test_create_listing(auth_client: AsyncClient) -> None:
    car_model = await CarModelFactory.create()
    req = {
        'car_model_id': str(car_model.id),
        'color': 'test',
        'price': 1,
        'latitude': 'test',
        'longitude': 'test',
        'vin': 'test',
        'license_plate': 'test',
        'options': [
            {
                'title': 'test1',
            },
            {
                'title': 'test2',
            },
        ],
    }
    response = await auth_client.post('/api/listings/', json=req)
    assert response.status_code == status.HTTP_200_OK


async def test_create_listing_nf_carmodel(auth_client: AsyncClient) -> None:
    req = {
        'car_model_id': str(uuid4()),
        'color': 'test',
        'price': 1,
        'latitude': 'test',
        'longitude': 'test',
        'vin': 'test',
        'license_plate': 'test',
        'options': [
            {
                'title': 'test1',
            },
            {
                'title': 'test2',
            },
        ],
    }
    response = await auth_client.post('/api/listings/', json=req)
    assert response.status_code == status.HTTP_404_NOT_FOUND
