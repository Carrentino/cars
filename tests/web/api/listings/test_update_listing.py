from uuid import uuid4

from helpers.models.user import UserContext
from httpx import AsyncClient
from starlette import status

from src.web.api.listings.schemas import UpdateCarSchema, CarOption
from tests.factories.car import CarFactory


async def test_update_listing_ok(user_context: UserContext, auth_client: AsyncClient) -> None:
    req = UpdateCarSchema(
        color='test',
        price=123,
        latitude='test',
        longitude='test',
        options=[CarOption(title='test1'), CarOption(title='test2')],
    )
    car = await CarFactory.create(owner_id=user_context.user_id)
    response = await auth_client.put(f'/api/listings/{car.id}/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_update_listing_nf(user_context: UserContext, auth_client: AsyncClient) -> None:
    req = UpdateCarSchema(
        color='test',
        price=123,
        latitude='test',
        longitude='test',
        options=[CarOption(title='test1'), CarOption(title='test2')],
    )
    await CarFactory.create(owner_id=user_context.user_id)
    response = await auth_client.put(f'/api/listings/{uuid4()}/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_listing_not_owner(auth_client: AsyncClient) -> None:
    req = UpdateCarSchema(
        color='test',
        price=123,
        latitude='test',
        longitude='test',
        options=[CarOption(title='test1'), CarOption(title='test2')],
    )
    car = await CarFactory.create()
    response = await auth_client.put(f'/api/listings/{car.id}/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_403_FORBIDDEN
