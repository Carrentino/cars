from typing import Any
from uuid import UUID

from helpers.clients.http_client import BaseApiClient
from httpx import HTTPError


class ReviewsClient(BaseApiClient):
    _base_url = 'https://carrentino.ru/reviews/api/cars'

    async def get_reviews(self, car_id: UUID, token: str | None = None) -> list[Any] | Any:
        if token is not None:
            self.headers['X-Auth-Token'] = token
        response = await self.get(f'{self._base_url}/{car_id}/?limit=3&sort=popularity')
        try:
            response.raise_for_status()
        except HTTPError:
            return []
        return response.json()['data']
