from typing import Any
from uuid import UUID

from helpers.clients.http_client import BaseApiClient

from src.settings import get_settings


class ReviewsClient(BaseApiClient):
    _base_url = get_settings().reviews_url

    async def get_reviews(self, car_id: UUID, token: str | None = None) -> list[Any] | Any:
        if token is not None:
            self.headers['X-Auth-Token'] = token
        try:
            response = await self.get(self._base_url.join(f'{car_id}/?limit=3&sort=popularity'))
            response.raise_for_status()
        except:  # noqa: E722
            return ["Пинать Олега чтобы поднял сервис отзывов!!!"]
        return response.json()['data']
