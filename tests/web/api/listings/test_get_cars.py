from httpx import AsyncClient
from starlette import status

from src.db.enums.car import CarStatus
from tests.factories.car import CarFactory


async def test_get_cars(client: AsyncClient) -> None:
    await CarFactory.create(status=CarStatus.VERIFIED, color="black")
    await CarFactory.create(status=CarStatus.VERIFIED, color="black")
    await CarFactory.create(status=CarStatus.VERIFIED, color="white")
    response = await client.get('/api/listings/?limit=1&car__color=black')
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    assert len(json_resp['data']) == 1
    assert json_resp['total'] == 2
    assert json_resp['total_pages'] == 2
