from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from helpers.depends.auth import get_current_user, get_optional_user
from helpers.models.response import PaginatedResponse
from helpers.models.user import UserContext
from helpers.utils import get_paginated_response
from starlette.requests import Request

from src.errors.http import (
    UserIsNotVerifiedHttpError,
    CarNotFoundHttpError,
    UserIsNotOwnerHttpError,
    CarModelNotFoundHttpError,
)
from src.errors.service import UserIsNotVerifiedError, CarNotFoundError, UserIsNotOwnerError, CarModelNotFoundError
from src.services.car import CarService
from src.services.car_attachment import CarAttachmentService
from src.web.api.listings.schemas import CreateCarReq, CarResp, CarFilters, CarPaginatedResponse, RetrieveCarSchema
from src.web.depends.service import get_car_service, get_car_attachment_service

listings_router = APIRouter()


@listings_router.get('/{car_id}/')
async def get_current_car(
    request: Request,
    car_service: Annotated[CarService, Depends(get_car_service)],
    user_context: Annotated[UserContext | None, Depends(get_optional_user)],
    car_id: UUID,
) -> RetrieveCarSchema:
    try:
        return await car_service.get_current_car(car_id, user_context, request.headers.get('x-auth-token'))
    except CarNotFoundError:
        raise CarNotFoundHttpError from None


@listings_router.get('/', response_model=CarPaginatedResponse)
async def get_cars(
    filters: Annotated[CarFilters, Depends()],
    car_service: Annotated[CarService, Depends(get_car_service)],
) -> PaginatedResponse:
    cars, count = await car_service.get_cars(filters)
    return await get_paginated_response(cars, count, filters.limit, filters.offset)


@listings_router.post('/')
async def create_car(
    car_service: Annotated[CarService, Depends(get_car_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    req_data: CreateCarReq,
) -> CarResp:
    try:
        car_id = await car_service.create_car(user_context, req_data)
        return CarResp(id=str(car_id))
    except UserIsNotVerifiedError:
        raise UserIsNotVerifiedHttpError from None
    except CarModelNotFoundError:
        raise CarModelNotFoundHttpError from None


@listings_router.post('/{car_id}/add-attachments')
async def add_attachment_to_listing(
    car_attachment_service: Annotated[CarAttachmentService, Depends(get_car_attachment_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    attachments: list[UploadFile],
    car_id: str,
) -> CarResp:
    try:
        await car_attachment_service.add_attachments(user_context, UUID(car_id), attachments)
        return CarResp(id=str(car_id))
    except UserIsNotOwnerError:
        raise UserIsNotOwnerHttpError from None
    except CarNotFoundError:
        raise CarNotFoundHttpError from None
