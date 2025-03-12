from uuid import uuid4

from helpers.models.user import UserContext
from httpx import AsyncClient
from starlette import status

from tests.factories.car import CarFactory


async def test_delete_listing_ok(user_context: UserContext, auth_client: AsyncClient) -> None:
    car = await CarFactory.create(owner_id=user_context.user_id)
    response = await auth_client.delete(f'/api/listings/{car.id}/')
    assert response.status_code == status.HTTP_200_OK


async def test_delete_listing_nf(user_context: UserContext, auth_client: AsyncClient) -> None:
    await CarFactory.create(owner_id=user_context.user_id)
    response = await auth_client.delete(f'/api/listings/{uuid4()}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_listing_not_owner(auth_client: AsyncClient) -> None:
    car = await CarFactory.create()
    response = await auth_client.delete(f'/api/listings/{car.id}/')
    assert response.status_code == status.HTTP_403_FORBIDDEN
