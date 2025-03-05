from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File
from helpers.depends.auth import get_current_user
from helpers.models.user import UserContext

from src.errors.http import UserIsNotVerifiedHttpError
from src.errors.service import UserIsNotVerifiedError
from src.services.car import CarService
from src.web.depends.service import get_car_service
from src.web.listings.schemas import CreateCarReq, CreateCarResp

listings_router = APIRouter()


@listings_router.post('/')
async def create_car(
    car_service: Annotated[CarService, Depends(get_car_service)],
    user_context: Annotated[UserContext, Depends(get_current_user)],
    req_data: CreateCarReq,
    attachments: list[UploadFile] = File(...),
) -> CreateCarResp:
    try:
        car_id = await car_service.create_car(user_context, req_data, attachments)
        return CreateCarResp(id=car_id)
    except UserIsNotVerifiedError:
        raise UserIsNotVerifiedHttpError from None
