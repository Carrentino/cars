from typing import Annotated

from fastapi import Depends
from helpers.depends.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.brand import BrandRepository
from src.repositories.car import CarRepository
from src.repositories.car_attachment import CarAttachmentRepository
from src.repositories.car_model import CarModelRepository
from src.repositories.car_option import CarOptionRepository


async def get_car_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> CarRepository:
    return CarRepository(session)


async def get_car_attachment_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> CarAttachmentRepository:
    return CarAttachmentRepository(session)


async def get_car_option_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> CarOptionRepository:
    return CarOptionRepository(session)


async def get_car_model_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> CarModelRepository:
    return CarModelRepository(session)


async def get_brand_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> BrandRepository:
    return BrandRepository(session)
