from unittest.mock import AsyncMock, patch
from uuid import uuid4

from httpx import AsyncClient
from starlette import status

from src.db.enums.car import CarStatus
from tests.factories.car import CarFactory


@patch('src.integrations.reviews.ReviewsClient.get_reviews', new_callable=AsyncMock)
async def test_get_current_listing(mock_get_reviews: AsyncMock, client: AsyncClient) -> None:
    car = await CarFactory.create(status=CarStatus.VERIFIED)
    mock_get_reviews.return_value = []
    response = await client.get(f"/api/listings/{car.id}/")
    assert response.status_code == status.HTTP_200_OK


@patch('src.integrations.reviews.ReviewsClient.get_reviews', new_callable=AsyncMock)
async def test_get_current_listing_nf(mock_get_reviews: AsyncMock, client: AsyncClient) -> None:
    response = await client.get(f"/api/listings/{uuid4()}/")
    mock_get_reviews.return_value = []
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch('src.integrations.reviews.ReviewsClient.get_reviews', new_callable=AsyncMock)
async def test_get_current_listing_invalid_status(mock_get_reviews: AsyncMock, client: AsyncClient) -> None:
    car = await CarFactory.create(status=CarStatus.BANNED)
    mock_get_reviews.return_value = []
    response = await client.get(f"/api/listings/{car.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
