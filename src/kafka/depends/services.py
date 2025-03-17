from sqlalchemy.ext.asyncio import AsyncSession

from src.services.car import CarService
from src.web.depends.integrations import get_reviews_client
from src.web.depends.repository import get_car_repository, get_car_option_repository, get_car_model_repository


async def get_car_service(session: AsyncSession) -> CarService:
    return CarService(
        car_repository=await get_car_repository(session=session),
        car_option_repository=await get_car_option_repository(session=session),
        car_model_repository=await get_car_model_repository(session=session),
        reviews_client=await get_reviews_client(),
    )
