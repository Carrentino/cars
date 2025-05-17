from typing import Annotated

from fastapi import APIRouter, Depends
from helpers.models.response import PaginatedResponse
from helpers.utils import get_paginated_response

from src.services.brand import BrandService
from src.services.car_model import CarModelService
from src.web.api.readonly.schemas import BrandPaginatedResponse, CarModelPaginatedResponse
from src.web.depends.service import get_brand_service, get_car_model_service

brands_router = APIRouter()


@brands_router.get("/", response_model=BrandPaginatedResponse)
async def get_brands(
    brand_service: Annotated[BrandService, Depends(get_brand_service)],
    start: str = "",
    limit: int = 30,
    offset: int = 0,
) -> PaginatedResponse:
    res, count = await brand_service.get_brands(start, limit, offset)
    return await get_paginated_response(list(res), count, limit, offset)


car_models_router = APIRouter()


@car_models_router.get("/", response_model=CarModelPaginatedResponse)
async def get_car_modelo(
    car_model_service: Annotated[CarModelService, Depends(get_car_model_service)],
    start: str = "",
    limit: int = 30,
    offset: int = 0,
) -> PaginatedResponse:
    res, count = await car_model_service.get_car_models(start, limit, offset)
    return await get_paginated_response(list(res), count, limit, offset)
