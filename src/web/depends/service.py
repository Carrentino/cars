from typing import Annotated

from fastapi import Depends

from src.repositories.car import CarRepository
from src.repositories.car_attachment import CarAttachmentRepository
from src.repositories.car_option import CarOptionRepository
from src.services.car import CarService
from src.web.depends.repository import (get_car_repository,
                                        get_car_attachment_repository,
                                        get_car_option_repository)


async def get_car_service(
    car_repository: Annotated[
        CarRepository, Depends(get_car_repository)],
    car_attachment_repository: Annotated[
        CarAttachmentRepository, Depends(get_car_attachment_repository)],
    car_option_repository: Annotated[
        CarOptionRepository, Depends(get_car_option_repository)],
) -> CarService:
    return CarService(
        car_repository=car_repository,
        car_attachment_repository=car_attachment_repository,
        car_option_repository=car_option_repository
    )
