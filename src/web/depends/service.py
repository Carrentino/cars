from typing import Annotated

from fastapi import Depends

from src.repositories.car import CarRepository
from src.repositories.car_attachment import CarAttachmentRepository
from src.repositories.car_model import CarModelRepository
from src.repositories.car_option import CarOptionRepository
from src.services.car import CarService
from src.services.car_attachment import CarAttachmentService
from src.web.depends.repository import (
    get_car_repository,
    get_car_attachment_repository,
    get_car_option_repository,
    get_car_model_repository,
)


async def get_car_service(
    car_repository: Annotated[CarRepository, Depends(get_car_repository)],
    car_option_repository: Annotated[CarOptionRepository, Depends(get_car_option_repository)],
    car_model_repository: Annotated[CarModelRepository, Depends(get_car_model_repository)],
) -> CarService:
    return CarService(
        car_repository=car_repository,
        car_model_repository=car_model_repository,
        car_option_repository=car_option_repository,
    )


async def get_car_attachment_service(
    car_attachment_repository: Annotated[CarAttachmentRepository, Depends(get_car_attachment_repository)],
    car_repository: Annotated[CarRepository, Depends(get_car_repository)],
) -> CarAttachmentService:
    return CarAttachmentService(car_attachment_repository=car_attachment_repository, car_repository=car_repository)
